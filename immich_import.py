import os
import requests
import argparse

def get_headers(api_key):
    return {
        "x-api-key": f"{api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def get_album_id(api_url, headers, album_name):
    try:
        resp = requests.get(f"{api_url}/albums", headers=headers)
        resp.raise_for_status()
        albums = resp.json()
        for album in albums:
            if album['albumName'] == album_name:
                return album['id']
    except:
        pass
    return None

def create_album(api_url, headers, album_name, dry_run=False):
    if dry_run:
        print(f"[DRY RUN] Would create album '{album_name}'")
        return "SIMULATED_ALBUM_ID"
    data = {"albumName": album_name}
    resp = requests.post(f"{api_url}/albums", headers=headers, json=data)
    resp.raise_for_status()
    return resp.json()['id']

def find_asset_id(api_url, headers, filename):
    data = {"originalFileName": filename}
    resp = requests.post(f"{api_url}/search/metadata", headers=headers, json=data)
    resp.raise_for_status()
    results = resp.json()
    if results and 'assets' in results and results['assets'] and results['assets']['items'] and len(results['assets']['items']) == 1:
        print(results)
        return results['assets']['items'][0]['id']
    return None

def add_assets_to_album(api_url, headers, album_id, asset_ids, dry_run=False):
    if dry_run:
        print(f"[DRY RUN] Would add {len(asset_ids)} assets to album ID '{album_id}'")
        return
    data = {"ids": asset_ids}
    resp = requests.put(f"{api_url}/albums/{album_id}/assets", headers=headers, json=data)
    resp.raise_for_status()

def main(root_folder, api_url, api_key, dry_run=False):
    headers = get_headers(api_key)
    for album_name in os.listdir(root_folder):
        album_path = os.path.join(root_folder, album_name)
        if not os.path.isdir(album_path):
            continue
        print(f"\nProcessing album: {album_name}")
        album_id = get_album_id(api_url, headers, album_name)
        if not album_id:
            if dry_run:
                print(f"[DRY RUN] Would create album '{album_name}'...")
                album_id = "SIMULATED_ALBUM_ID"
            else:
                print(f"Creating album '{album_name}'...")
                album_id = create_album(api_url, headers, album_name)
        else:
            print(f"Album '{album_name}' already exists.")
        asset_ids = []
        for fname in os.listdir(album_path):
            fpath = os.path.join(album_path, fname)
            if not os.path.isfile(fpath):
                continue
            asset_id = find_asset_id(api_url, headers, fname)
            if asset_id:
                print(f"  Found asset for '{fname}': {asset_id}")
                asset_ids.append(asset_id)
            else:
                print(f"  WARNING: Asset not found in Immich for '{fname}'")
        if asset_ids:
            if dry_run:
                print(f"[DRY RUN] Would add {len(asset_ids)} assets to album '{album_name}'")
            else:
                print(f"Adding {len(asset_ids)} assets to album '{album_name}'...")
                add_assets_to_album(api_url, headers, album_id, asset_ids)
        else:
            print(f"No assets to add for album '{album_name}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create Immich albums from folder structure and add existing images by filename.")
    parser.add_argument("--root-folder", required=True, help="Root folder containing album subfolders")
    parser.add_argument("--immich-url", required=True, help="Base URL of your Immich instance, e.g. http://localhost:2283/api")
    parser.add_argument("--api-key", required=True, help="Immich API key or access token")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without making changes")
    args = parser.parse_args()
    main(args.root_folder, args.immich_url, args.api_key, dry_run=args.dry_run)
