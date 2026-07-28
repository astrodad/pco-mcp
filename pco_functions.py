"""
Core PCO functions without MCP decorators.
"""
from pypco import PCO
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the PCO client with credentials from environment variables
pco = PCO(
    application_id=os.getenv("PCO_APPLICATION_ID"),
    secret=os.getenv("PCO_SECRET_KEY")
)

def get_service_types() -> list:
    """Fetch a list of service types from the Planning Center Online API."""
    response = pco.get('/services/v2/service_types')
    return response['data']

def get_plans(service_type_id: str) -> list:
    """Fetch a list of plans for a specific service type."""
    response = pco.get(f'/services/v2/service_types/{service_type_id}/plans?order=-updated_at')
    return response['data']

def get_plan_items(plan_id: str) -> list:
    """Fetch a list of items for a specific plan."""
    response = pco.get(f'/services/v2/plans/{plan_id}/items')
    return response['data']

def get_plan_team_members(plan_id: str) -> list:
    """Fetch a list of team members for a specific plan."""
    response = pco.get(f'/services/v2/plans/{plan_id}/team_members')
    return response['data']

def get_songs() -> list:
    """Fetch a list of songs from the Planning Center Online API."""
    response = pco.get('/services/v2/songs?per_page=200&where[hidden]=false')
    return response['data']

def get_all_arrangements_for_song(song_id: str) -> list:
    """
    Get a list of all the arrangements for a particular song from the Planning Center Online API.

    Args:
        song_id (str): The ID for the song.
    """
    response = pco.get(f'/services/v2/songs/{song_id}/arrangements')
    return response['data']

def get_arrangement_for_song(song_id: str, arrangement_id: str) -> dict:
    """
    Get information for a particular arrangement of a song from the Planning Center Online API.

    Args:
        song_id (str): The ID for the song.
        arrangement_id (str): The ID for the arrangement within a song.
    """
    response = pco.get(f'/services/v2/songs/{song_id}/arrangements/{arrangement_id}')
    return response['data']

def get_keys_for_arrangement_of_song(song_id: str, arrangement_id: str) -> list:
    """
    Get a list of keys available for a particular song ID and arrangement ID from the Planning Center Online API.

    Args:
        song_id (str): The ID for the song.
        arrangement_id (str): The ID for the arrangement within a song.
    """
    response = pco.get(f'/services/v2/songs/{song_id}/arrangements/{arrangement_id}/keys')
    return response['data']

def create_key_for_arrangement(
    song_id: str,
    arrangement_id: str,
    starting_key: str,
    ending_key: str = None,
    name: str = None,
) -> dict:
    """
    Add a new key to a particular arrangement of a song.

    Whether a key is minor is inferred from its notation (e.g. "Dm" for D minor),
    not passed as a separate flag - the PCO API rejects starting_minor/ending_minor
    as explicit attributes on create.

    Args:
        song_id (str): The ID for the song.
        arrangement_id (str): The ID for the arrangement within a song.
        starting_key (str): The key the arrangement starts in (e.g. "G" or "Dm").
        ending_key (str, optional): The key the arrangement modulates to, if any.
        name (str, optional): A display name for the key (e.g. "Capo 3").

    Returns:
        dict: The created key data.
    """
    attributes = {"starting_key": starting_key}
    if ending_key is not None:
        attributes["ending_key"] = ending_key
    if name is not None:
        attributes["name"] = name

    body = pco.template('Key', attributes)
    response = pco.post(f'/services/v2/songs/{song_id}/arrangements/{arrangement_id}/keys', body)
    return response['data']

def create_song(title: str, ccli: str = None) -> dict:
    """
    Create a new song in Planning Center Online.

    Args:
        title (str): The title of the song.
        ccli (str, optional): The CCLI number for the song.

    Returns:
        dict: The created song data.
    """
    attributes = {"title": title}
    if ccli:
        attributes["ccli_number"] = ccli

    body = pco.template('Song', attributes)
    response = pco.post('/services/v2/songs', body)
    return response['data']

def find_song_by_title(title: str) -> list:
    """
    Find songs by title.

    Args:
        title (str): The title of the song to search for.

    Returns:
        list: List of songs matching the title.
    """
    response = pco.get(f'/services/v2/songs?where[title]={title}&where[hidden]=false')
    return response['data']

def get_song(song_id: str) -> dict:
    """
    Fetch details for a specific song.

    Args:
        song_id (str): The ID of the song.
    """
    response = pco.get(f'/services/v2/songs/{song_id}')
    return response['data']

def assign_tags_to_song(song_id: str, tag_names: list[str], replace: bool = False) -> dict:
    """
    Assign tags to a specific song. By default, this will ADD the specified tags to any existing tags.
    Set replace=True to replace all existing tags with the specified tags.

    Args:
        song_id (str): The ID of the song.
        tag_names (list[str]): List of tag names to assign to the song.
        replace (bool, optional): If True, replace all existing tags. If False (default), add to existing tags.

    Returns:
        dict: Success status and message.
    """
    existing_tag_ids = set()

    if not replace:
        # Get existing tags for the song
        existing_tags_response = pco.get(f'/services/v2/songs/{song_id}/tags')
        existing_tags = existing_tags_response.get('data', [])

        # Build a set of existing tag IDs to avoid duplicates
        existing_tag_ids = {tag['id'] for tag in existing_tags}

        # Start with existing tags in the tag_data list
        tag_data = [{"type": "Tag", "id": tag_id} for tag_id in existing_tag_ids]
    else:
        # Start with an empty tag list for replacement
        tag_data = []

    # Get all tag groups with their tags included
    tag_groups_response = pco.get('/services/v2/tag_groups?include=tags&filter=song')

    # Extract tags from the included section
    included_tags = tag_groups_response.get('included', [])

    # Find the tag IDs for the requested tag names and add new ones
    new_tags_added = 0
    for tag_name in tag_names:
        for tag in included_tags:
            if tag['type'] == 'Tag' and tag['attributes']['name'].lower() == tag_name.lower():
                tag_id = tag['id']
                # Only add if not already in the list
                if tag_id not in existing_tag_ids:
                    tag_data.append({
                        "type": "Tag",
                        "id": tag_id
                    })
                    existing_tag_ids.add(tag_id)
                    new_tags_added += 1
                break

    if not replace and new_tags_added == 0:
        return {"success": True, "message": "No new tags to add (tags already exist or not found)"}

    if replace and len(tag_data) == 0:
        return {"success": True, "message": "No valid tags found to assign"}

    # Build the request body
    body = {
        "data": {
            "type": "TagAssignment",
            "attributes": {},
            "relationships": {
                "tags": {
                    "data": tag_data
                }
            }
        }
    }

    # Make the POST request
    response = pco.post(f'/services/v2/songs/{song_id}/assign_tags', body)

    # A 204 status means success with no content
    if replace:
        return {"success": True, "message": f"Successfully replaced tags for song {song_id} with {len(tag_data)} tag(s)"}
    else:
        return {"success": True, "message": f"Successfully assigned {new_tags_added} new tag(s) to song {song_id} (total: {len(tag_data)} tags)"}

def find_songs_by_tags(tag_names: list[str]) -> list:
    """
    Find songs that have all of the specified tags.

    Args:
        tag_names (list[str]): List of tag names to filter songs by. Songs must have all specified tags.
    """
    # Get all tag groups with their tags included
    tag_groups_response = pco.get('/services/v2/tag_groups?include=tags&filter=song')

    # Extract tags from the included section
    included_tags = tag_groups_response.get('included', [])

    # Find the tag IDs for the requested tag names
    tag_ids = []
    for tag_name in tag_names:
        for tag in included_tags:
            if tag['type'] == 'Tag' and tag['attributes']['name'].lower() == tag_name.lower():
                tag_ids.append(tag['id'])
                break

    if not tag_ids:
        return []

    # Build the query string with tag filters
    # Multiple tag filters create an AND condition
    tag_filters = '&'.join([f'where[song_tag_ids]={tag_id}' for tag_id in tag_ids])
    query = f'/services/v2/songs?per_page=200&where[hidden]=false&{tag_filters}'

    response = pco.get(query)
    return response['data']
