from fastmcp import FastMCP
from pco_functions import (
    get_service_types as _get_service_types,
    get_plans as _get_plans,
    get_plan_items as _get_plan_items,
    get_plan_team_members as _get_plan_team_members,
    create_plan as _create_plan,
    update_plan as _update_plan,
    delete_plan as _delete_plan,
    delete_plan_item as _delete_plan_item,
    add_header_to_plan as _add_header_to_plan,
    add_song_to_plan as _add_song_to_plan,
    add_item_to_plan as _add_item_to_plan,
    get_songs as _get_songs,
    get_all_arrangements_for_song as _get_all_arrangements_for_song,
    get_arrangement_for_song as _get_arrangement_for_song,
    get_keys_for_arrangement_of_song as _get_keys_for_arrangement_of_song,
    create_key_for_arrangement as _create_key_for_arrangement,
    create_song as _create_song,
    find_song_by_title as _find_song_by_title,
    get_song as _get_song,
    assign_tags_to_song as _assign_tags_to_song,
    find_songs_by_tags as _find_songs_by_tags
)

mcp = FastMCP("PCO Services MCP Server")

@mcp.tool()
def get_service_types() -> list:
    """Fetch a list of service types from the Planning Center Online API."""
    return _get_service_types()

@mcp.tool()
def get_plans(service_type_id: str) -> list:
    """
    Fetch a list of plans for a specific service type.

    Args:
        service_type_id (str): The ID of the service type.
    """
    return _get_plans(service_type_id)

@mcp.tool()
def get_plan_items(plan_id: str) -> list:
    """
    Fetch a list of items for a specific plan.

    Args:
        plan_id (str): The ID of the plan.
    """
    return _get_plan_items(plan_id)

@mcp.tool()
def get_plan_team_members(plan_id: str) -> list:
    """
    Fetch a list of team members for a specific plan.

    Args:
        plan_id (str): The ID of the plan.
    """
    return _get_plan_team_members(plan_id)

@mcp.tool()
def create_plan(service_type_id: str, title: str = None) -> dict:
    """
    Create a new plan within a service type.

    Args:
        service_type_id (str): The ID of the service type to create the plan under.
        title (str, optional): The title of the plan. If omitted, the plan is untitled
            and displays by its date instead (PCO's default behavior).

    Returns:
        dict: The created plan data.
    """
    return _create_plan(service_type_id, title)

@mcp.tool()
def update_plan(service_type_id: str, plan_id: str, title: str = None) -> dict:
    """
    Update an existing plan's title.

    Args:
        service_type_id (str): The ID of the service type the plan belongs to.
        plan_id (str): The ID of the plan to update.
        title (str, optional): The new title for the plan.

    Returns:
        dict: The updated plan data.
    """
    return _update_plan(service_type_id, plan_id, title)

@mcp.tool()
def delete_plan(service_type_id: str, plan_id: str) -> dict:
    """
    Delete a plan. This also deletes all of its items.

    Args:
        service_type_id (str): The ID of the service type the plan belongs to.
        plan_id (str): The ID of the plan to delete.

    Returns:
        dict: Success status and message.
    """
    return _delete_plan(service_type_id, plan_id)

@mcp.tool()
def delete_plan_item(service_type_id: str, plan_id: str, item_id: str) -> dict:
    """
    Delete a single item (song, header, or generic entry) from a plan.

    Args:
        service_type_id (str): The ID of the service type the plan belongs to.
        plan_id (str): The ID of the plan the item belongs to.
        item_id (str): The ID of the item to delete.

    Returns:
        dict: Success status and message.
    """
    return _delete_plan_item(service_type_id, plan_id, item_id)

@mcp.tool()
def add_header_to_plan(service_type_id: str, plan_id: str, title: str, sequence: int = None) -> dict:
    """
    Add a header entry to a plan (e.g. a section label like "Opening" or "Communion").

    Args:
        service_type_id (str): The ID of the service type the plan belongs to.
        plan_id (str): The ID of the plan to add the header to.
        title (str): The header's label.
        sequence (int, optional): Position in the plan's item order. If omitted, the
            header is appended to the end of the plan.

    Returns:
        dict: The created plan item data.
    """
    return _add_header_to_plan(service_type_id, plan_id, title, sequence)

@mcp.tool()
def add_song_to_plan(
    service_type_id: str,
    plan_id: str,
    song_id: str,
    arrangement_id: str = None,
    key_id: str = None,
    title: str = None,
    sequence: int = None,
) -> dict:
    """
    Add a song entry to a plan.

    Args:
        service_type_id (str): The ID of the service type the plan belongs to.
        plan_id (str): The ID of the plan to add the song to.
        song_id (str): The ID of the song to add.
        arrangement_id (str, optional): The ID of the specific arrangement to use.
        key_id (str, optional): The ID of a key (from get_keys_for_arrangement_of_song,
            or newly created via create_key_for_arrangement) to assign to this item.
            Requires arrangement_id - PCO silently drops the key otherwise.
        title (str, optional): Display title for the item. Defaults to the song's title -
            PCO does not fill this in automatically like the web UI does.
        sequence (int, optional): Position in the plan's item order. If omitted, the
            item is appended to the end of the plan.

    Returns:
        dict: The created plan item data.
    """
    return _add_song_to_plan(service_type_id, plan_id, song_id, arrangement_id, key_id, title, sequence)

@mcp.tool()
def add_item_to_plan(service_type_id: str, plan_id: str, title: str, sequence: int = None) -> dict:
    """
    Add a generic entry to a plan (anything that isn't a song or a header,
    e.g. "Welcome" or "Announcements").

    Args:
        service_type_id (str): The ID of the service type the plan belongs to.
        plan_id (str): The ID of the plan to add the item to.
        title (str): The item's title.
        sequence (int, optional): Position in the plan's item order. If omitted, the
            item is appended to the end of the plan.

    Returns:
        dict: The created plan item data.
    """
    return _add_item_to_plan(service_type_id, plan_id, title, sequence)

@mcp.tool()
def get_songs() -> list:
    """Fetch a list of songs from the Planning Center Online API."""
    return _get_songs()

@mcp.tool()
def get_all_arrangements_for_song(song_id: str) -> list:
    """
    Get a list of all the arrangements for a particular song from the Planning Center Online API.

    Args:
        song_id (str): The ID for the song.
    """
    return _get_all_arrangements_for_song(song_id)

@mcp.tool()
def get_arrangement_for_song(song_id: str, arrangement_id: str) -> dict:
    """
    Get information for a particular song from the Planning Center Online API.

    Args:
        song_id (str): The ID for the song.
        arrangement_id (str): The ID for the arrangement within a song.
    """
    return _get_arrangement_for_song(song_id, arrangement_id)

@mcp.tool()
def get_keys_for_arrangement_of_song(song_id: str, arrangement_id: str) -> list:
    """
    Get a list of keys available for a particular song ID and arrangement ID from the Planning Center Online API.

    Args:
        song_id (str): The ID for the song.
        arrangement_id (str): The ID for the arrangement within a song.
    """
    return _get_keys_for_arrangement_of_song(song_id, arrangement_id)

@mcp.tool()
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
    return _create_key_for_arrangement(song_id, arrangement_id, starting_key, ending_key, name)

@mcp.tool()
def create_song(title: str, ccli: str = None) -> dict:
    """
    Create a new song in Planning Center Online.

    Args:
        title (str): The title of the song.
        ccli (str, optional): The CCLI number for the song.

    Returns:
        dict: The created song data.
    """
    return _create_song(title, ccli)

@mcp.tool()
def find_song_by_title(title: str) -> list:
    """
    Find songs by title.

    Args:
        title (str): The title of the song to search for.

    Returns:
        list: List of songs matching the title.
    """
    return _find_song_by_title(title)

@mcp.tool()
def get_song(song_id: str) -> dict:
    """
    Fetch details for a specific song.

    Args:
        song_id (str): The ID of the song.
    """
    return _get_song(song_id)

@mcp.tool()
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
    return _assign_tags_to_song(song_id, tag_names, replace)

@mcp.tool()
def find_songs_by_tags(tag_names: list[str]) -> list:
    """
    Find songs that have all of the specified tags.

    Args:
        tag_names (list[str]): List of tag names to filter songs by. Songs must have all specified tags.
    """
    return _find_songs_by_tags(tag_names)



if __name__ == "__main__":
    # Example usage of the tools
    print("PCO Services MCP Server - CLI Test Mode")
    
    # Test getting service types
    print("\nFetching service types...")
    service_types = get_service_types()
    print(f"Found {len(service_types)} service types")
    print(service_types)
    
    if service_types:
        # Test getting plans for the first service type
        service_type_id = service_types[0].get('id')
        print(f"\nFetching plans for service type ID: {service_type_id}")
        plans = get_plans(service_type_id)
        print(f"Found {len(plans)} plans")
        
        if plans:
            # Test getting plan items for the first plan
            plan_id = plans[0].get('id')
            print(f"\nFetching items for plan ID: {plan_id}")
            items = get_plan_items(plan_id)
            print(f"Found {len(items)} items")
            
            # Test getting team members for the first plan
            print(f"\nFetching team members for plan ID: {plan_id}")
            team_members = get_plan_team_members(plan_id)
            print(f"Found {len(team_members)} team members")
            
            if team_members:
                # Test getting assignments for the first team member
                team_member_id = team_members[0].get('id')
                print(f"\nFetching assignments for team member ID: {team_member_id}")
                # assignments = get_plan_team_member_assignments(plan_id, team_member_id)
                # print(f"Found {len(assignments)} assignments")
    
    # Test getting songs
    print("\nFetching songs...")
    songs = get_songs()
    print(f"Found {len(songs)} songs")
    
    if songs:
        # Test getting details for the first song
        song_id = songs[0].get('id')
        print(f"\nFetching details for song ID: {song_id}")
        song_details = get_song(song_id)
        print(f"Song details: {song_details.get('title')} by {song_details.get('author')}")
    
    # # Test iterating through plans
    # if service_types:
    #     service_type_id = service_types[0].get('id')
    #     print(f"\nIterating through plans for service type ID: {service_type_id}")
    #     plans = iterate_through_plans(service_type_id)
    #     print(f"Found {len(plans)} plans through iteration")
    
    print("\nCLI test completed.")
