"""
Admin panel routes
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from database import (
    SessionLocal, Lead, Conversation, 
    get_analytics_stats, get_user_conversation_history
)
import json

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard():
    """Serve admin dashboard"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AutoStream Admin Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            .card h3 { color: #667eea; margin-bottom: 10px; }
            .card .value { font-size: 32px; font-weight: bold; color: #333; }
            .card .label { color: #666; font-size: 14px; }
            .table-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            table { width: 100%; border-collapse: collapse; }
            th { background: #f5f5f5; padding: 12px; text-align: left; font-weight: 600; }
            td { padding: 12px; border-bottom: 1px solid #eee; }
            tr:hover { background: #f9f9f9; }
            .btn { background: #667eea; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
            .btn:hover { background: #764ba2; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 AutoStream Admin Dashboard</h1>
                <p>Real-time business metrics</p>
            </div>
            
            <div class="grid" id="metrics"></div>
            
            <div class="table-container">
                <h2>Recent Leads</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Platform</th>
                            <th>Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="leads-table"></tbody>
                </table>
            </div>
        </div>
        
        <script>
            async function loadDashboard() {
                const response = await fetch('/analytics/summary');
                const data = await response.json();
                const stats = data.analytics;
                
                document.getElementById('metrics').innerHTML = `
                    <div class="card">
                        <h3>Total Leads</h3>
                        <div class="value">${stats.total_leads}</div>
                        <div class="label">Active leads in system</div>
                    </div>
                    <div class="card">
                        <h3>Conversations</h3>
                        <div class="value">${stats.total_conversations}</div>
                        <div class="label">Total messages</div>
                    </div>
                    <div class="card">
                        <h3>New Leads</h3>
                        <div class="value">${stats.new_leads}</div>
                        <div class="label">This month</div>
                    </div>
                `;
            }
            
            loadDashboard();
            setInterval(loadDashboard, 5000);
        </script>
    </body>
    </html>
    """

@router.get("/api/leads")
async def get_all_leads():
    """Get all leads"""
    db = SessionLocal()
    try:
        leads = db.query(Lead).all()
        return JSONResponse([
            {
                'id': lead.id,
                'name': lead.name,
                'email': lead.email,
                'platform': lead.platform,
                'created_at': str(lead.created_at),
                'status': lead.status
            }
            for lead in leads
        ])
    finally:
        db.close()

@router.get("/api/conversations/{user_id}")
async def get_user_conversations(user_id: str):
    """Get all conversations for a user"""
    conversations = get_user_conversation_history(user_id, limit=100)
    return JSONResponse([
        {
            'message': conv.message,
            'response': conv.response,
            'timestamp': str(conv.created_at),
            'channel': conv.channel
        }
        for conv in conversations
    ])

@router.get("/api/export/leads")
async def export_leads():
    """Export leads as CSV"""
    db = SessionLocal()
    try:
        leads = db.query(Lead).all()
        csv_content = "Name,Email,Platform,Created At,Status\n"
        for lead in leads:
            csv_content += f"{lead.name},{lead.email},{lead.platform},{lead.created_at},{lead.status}\n"
        
        return {
            "filename": "leads_export.csv",
            "content": csv_content
        }
    finally:
        db.close()
