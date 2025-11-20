import os
import requests
from fastmcp import FastMCP

mcp = FastMCP(name="ActiveCampaign")


@mcp.tool
def create_campaign(
    name: str,
    subject: str,
    from_name: str,
    from_email: str,
    reply_email: str,
    html_content: str,
    list_ids: list[int],
    campaign_type: str = "single",
    status: int = 0,
    send_date: str = None
) -> dict:
    """
    Create a new email campaign in ActiveCampaign.
    
    Args:
        name: Internal campaign name
        subject: Email subject line
        from_name: Sender name
        from_email: Sender email address
        reply_email: Reply-to email address
        html_content: HTML email content
        list_ids: List of contact list IDs to send to
        campaign_type: Type of campaign (single/recurring/split/responder)
        status: 0 for draft, 1 for scheduled
        send_date: When to send (format: 'YYYY-MM-DD HH:MM:SS')
    
    Returns:
        Campaign creation response with campaign ID
    """
    
    api_url = os.getenv('ACTIVECAMPAIGN_URL')
    api_key = os.getenv('ACTIVECAMPAIGN_API_KEY')
    
    if not api_url or not api_key:
        return {"error": "Missing ACTIVECAMPAIGN_URL or ACTIVECAMPAIGN_API_KEY environment variables"}
    
    endpoint = f"{api_url}/admin/api.php"
    
    post_data = {
        'api_action': 'campaign_create',
        'api_key': api_key,
        'api_output': 'json',
        'type': campaign_type,
        'name': name,
        'subject': subject,
        'fromname': from_name,
        'fromemail': from_email,
        'reply2': reply_email,
        'htmlcontent': html_content,
        'status': status,
    }
    
    for list_id in list_ids:
        post_data[f'p[{list_id}]'] = list_id
    
    if send_date and status == 1:
        post_data['sdate'] = send_date
    
    try:
        response = requests.post(
            endpoint,
            data=post_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def get_campaign(campaign_id: int) -> dict:
    """
    Get campaign details by ID.
    
    Args:
        campaign_id: The campaign ID
    
    Returns:
        Campaign details
    """
    api_url = os.getenv('ACTIVECAMPAIGN_URL')
    api_key = os.getenv('ACTIVECAMPAIGN_API_KEY')
    
    if not api_url or not api_key:
        return {"error": "Missing environment variables"}
    
    endpoint = f"{api_url}/admin/api.php"
    
    params = {
        'api_action': 'campaign_report_totals',
        'api_key': api_key,
        'api_output': 'json',
        'campaignid': campaign_id
    }
    
    try:
        response = requests.get(endpoint, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def list_campaigns() -> dict:
    """
    List all campaigns in ActiveCampaign.
    
    Returns:
        List of campaigns
    """
    api_url = os.getenv('ACTIVECAMPAIGN_URL')
    api_key = os.getenv('ACTIVECAMPAIGN_API_KEY')
    
    if not api_url or not api_key:
        return {"error": "Missing environment variables"}
    
    endpoint = f"{api_url}/admin/api.php"
    
    params = {
        'api_action': 'campaign_list',
        'api_key': api_key,
        'api_output': 'json'
    }
    
    try:
        response = requests.get(endpoint, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
