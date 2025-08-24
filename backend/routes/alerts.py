from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
import json
import uuid
from datetime import datetime
from utils.config import settings

router = APIRouter()

# Pydantic models for request validation
class AlertRequest(BaseModel):
    alert_type: str  # "contamination", "health_risk", "cleanup_required"
    priority: str    # "low", "medium", "high", "critical"
    location: Dict[str, float]  # {"latitude": float, "longitude": float}
    description: str
    detection_data: Optional[Dict] = None
    estimated_impact: Optional[Dict] = None
    user_id: Optional[str] = None

class NotificationRequest(BaseModel):
    recipient_type: str  # "authorities", "community", "emergency"
    message: str
    location: Dict[str, float]
    alert_id: str
    urgent: bool = False

class DroneDeploymentRequest(BaseModel):
    location: Dict[str, float]
    mission_type: str  # "verification", "monitoring", "cleanup_assessment"
    priority: str
    requester_id: Optional[str] = None

@router.post("/create-alert")
async def create_environmental_alert(alert: AlertRequest, background_tasks: BackgroundTasks):
    """
    Create environmental alert and notify relevant authorities
    """
    try:
        # Generate unique alert ID
        alert_id = f"ALERT_{uuid.uuid4().hex[:8].upper()}"
        
        # Validate alert type and priority
        valid_types = ["contamination", "health_risk", "cleanup_required", "water_quality", "illegal_dumping"]
        valid_priorities = ["low", "medium", "high", "critical"]
        
        if alert.alert_type not in valid_types:
            raise HTTPException(status_code=400, detail=f"Invalid alert type. Must be one of: {valid_types}")
        
        if alert.priority not in valid_priorities:
            raise HTTPException(status_code=400, detail=f"Invalid priority. Must be one of: {valid_priorities}")
        
        # Calculate response time based on priority
        response_times = {
            "critical": "15 minutes",
            "high": "2 hours",
            "medium": "24 hours", 
            "low": "72 hours"
        }
        
        # Determine notification recipients based on alert type and priority
        notification_targets = []
        
        if alert.priority in ["critical", "high"]:
            notification_targets.extend([
                "environmental_authority",
                "health_department",
                "local_government"
            ])
        
        if alert.alert_type == "health_risk":
            notification_targets.append("public_health_office")
        
        if alert.alert_type == "illegal_dumping":
            notification_targets.append("pollution_control_board")
        
        # Create alert record
        alert_record = {
            "alert_id": alert_id,
            "type": alert.alert_type,
            "priority": alert.priority,
            "status": "active",
            "location": alert.location,
            "description": alert.description,
            "detection_data": alert.detection_data,
            "estimated_impact": alert.estimated_impact,
            "created_at": datetime.now().isoformat(),
            "expected_response_time": response_times[alert.priority],
            "notification_targets": notification_targets,
            "user_id": alert.user_id
        }
        
        # Add background task to send notifications
        background_tasks.add_task(
            send_alert_notifications,
            alert_record,
            notification_targets
        )
        
        # Generate recommendations based on alert type
        recommendations = generate_alert_recommendations(alert.alert_type, alert.priority)
        
        return {
            "success": True,
            "alert_id": alert_id,
            "status": "created",
            "priority": alert.priority,
            "expected_response_time": response_times[alert.priority],
            "notification_sent": len(notification_targets) > 0,
            "notification_targets": notification_targets,
            "recommendations": recommendations,
            "follow_up_actions": generate_follow_up_actions(alert.alert_type, alert.priority),
            "created_at": alert_record["created_at"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create alert: {str(e)}")

@router.post("/notify-authorities")
async def notify_authorities(notification: NotificationRequest, background_tasks: BackgroundTasks):
    """
    Send notifications to relevant authorities
    """
    try:
        # Validate recipient type
        valid_recipients = [
            "authorities", "community", "emergency", "cleanup_crew", 
            "health_department", "environmental_agency"
        ]
        
        if notification.recipient_type not in valid_recipients:
            raise HTTPException(status_code=400, detail="Invalid recipient type")
        
        # Generate notification ID
        notification_id = f"NOTIF_{uuid.uuid4().hex[:8].upper()}"
        
        # Determine specific contacts based on recipient type
        contacts = get_notification_contacts(notification.recipient_type)
        
        # Create notification record
        notification_record = {
            "notification_id": notification_id,
            "alert_id": notification.alert_id,
            "recipient_type": notification.recipient_type,
            "message": notification.message,
            "location": notification.location,
            "urgent": notification.urgent,
            "contacts": contacts,
            "status": "sending",
            "created_at": datetime.now().isoformat()
        }
        
        # Add background task to actually send notifications
        background_tasks.add_task(
            process_notifications,
            notification_record
        )
        
        return {
            "success": True,
            "notification_id": notification_id,
            "recipient_type": notification.recipient_type,
            "contacts_notified": len(contacts),
            "delivery_method": "email, sms, webhook" if notification.urgent else "email",
            "estimated_delivery_time": "2-5 minutes" if notification.urgent else "5-15 minutes",
            "status": "queued_for_delivery"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

@router.post("/deploy-drone")
async def deploy_verification_drone(deployment: DroneDeploymentRequest):
    """
    Deploy drone for verification or monitoring (FAKE but realistic demo)
    """
    try:
        # Generate deployment ID
        deployment_id = f"DRONE_{uuid.uuid4().hex[:6].upper()}"
        
        # Validate mission type
        valid_missions = ["verification", "monitoring", "cleanup_assessment", "real_time_tracking"]
        if deployment.mission_type not in valid_missions:
            raise HTTPException(status_code=400, detail="Invalid mission type")
        
        # Calculate mission parameters
        mission_duration = {
            "verification": "15-30 minutes",
            "monitoring": "45-60 minutes", 
            "cleanup_assessment": "20-40 minutes",
            "real_time_tracking": "2-4 hours"
        }
        
        battery_required = {
            "verification": "25%",
            "monitoring": "60%",
            "cleanup_assessment": "35%",
            "real_time_tracking": "90%"
        }
        
        # Mock drone selection based on mission requirements
        available_drones = [
            {
                "drone_id": "SAT-DRONE-001",
                "type": "multispectral",
                "battery": "85%",
                "location": "Base Station Alpha",
                "distance_km": 2.3
            },
            {
                "drone_id": "SAT-DRONE-002", 
                "type": "thermal_imaging",
                "battery": "92%",
                "location": "Mobile Unit 1",
                "distance_km": 5.7
            }
        ]
        
        # Select best drone
        selected_drone = available_drones[0]  # Mock selection logic
        
        # Calculate ETA and mission timeline
        eta_minutes = round(selected_drone["distance_km"] * 2.5 + 5)  # Travel time + setup
        
        deployment_record = {
            "deployment_id": deployment_id,
            "mission_type": deployment.mission_type,
            "priority": deployment.priority,
            "location": deployment.location,
            "selected_drone": selected_drone,
            "status": "dispatched",
            "eta_minutes": eta_minutes,
            "expected_duration": mission_duration[deployment.mission_type],
            "battery_required": battery_required[deployment.mission_type],
            "mission_parameters": {
                "altitude_m": 50,
                "grid_pattern": True,
                "image_resolution": "4K",
                "sensors": ["optical", "multispectral", "thermal"]
            },
            "created_at": datetime.now().isoformat(),
            "requester_id": deployment.requester_id
        }
        
        return {
            "success": True,
            "deployment_id": deployment_id,
            "status": "mission_dispatched",
            "selected_drone": selected_drone,
            "eta": f"{eta_minutes} minutes",
            "expected_completion": mission_duration[deployment.mission_type],
            "live_tracking_url": f"https://satmap.org/drone-tracking/{deployment_id}",
            "mission_details": deployment_record["mission_parameters"],
            "next_update": "5 minutes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drone deployment failed: {str(e)}")

@router.get("/alert-status/{alert_id}")
async def get_alert_status(alert_id: str):
    """
    Get current status of an environmental alert
    """
    try:
        # Mock alert status lookup (in production, would query database)
        statuses = ["active", "investigating", "cleanup_scheduled", "resolved", "false_alarm"]
        current_status = f"investigating"  # Mock status
        
        # Mock timeline
        timeline = [
            {
                "timestamp": "2025-08-24T10:30:00Z",
                "event": "alert_created",
                "description": "Environmental alert created by user",
                "actor": "system"
            },
            {
                "timestamp": "2025-08-24T10:32:00Z",
                "event": "authorities_notified",
                "description": "Notifications sent to environmental authorities",
                "actor": "notification_system"
            },
            {
                "timestamp": "2025-08-24T10:45:00Z",
                "event": "investigation_started",
                "description": "Field team assigned to investigate",
                "actor": "environmental_authority"
            }
        ]
        
        return {
            "alert_id": alert_id,
            "current_status": current_status,
            "priority": "high",
            "created_at": "2025-08-24T10:30:00Z",
            "last_updated": "2025-08-24T10:45:00Z",
            "assigned_team": "Environmental Response Team Alpha",
            "estimated_resolution": "24-48 hours",
            "timeline": timeline,
            "current_actions": [
                "Field verification in progress",
                "Contamination assessment scheduled",
                "Community notifications prepared"
            ],
            "contact_info": {
                "case_officer": "Dr. Sarah Johnson",
                "phone": "+91-11-2345-6789",
                "email": "sarah.j@environmentalresponse.gov.in"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get alert status: {str(e)}")

@router.get("/notification-history")
async def get_notification_history(
    alert_id: Optional[str] = None,
    recipient_type: Optional[str] = None,
    limit: int = 50
):
    """
    Get notification history and delivery status
    """
    try:
        # Mock notification history
        notifications = []
        
        for i in range(min(limit, 20)):
            notification = {
                "notification_id": f"NOTIF_{uuid.uuid4().hex[:8].upper()}",
                "alert_id": alert_id or f"ALERT_{uuid.uuid4().hex[:8].upper()}",
                "recipient_type": recipient_type or "authorities",
                "message": "Environmental contamination detected - immediate attention required",
                "delivery_status": "delivered",
                "delivery_method": "email,sms",
                "sent_at": "2025-08-24T10:32:00Z",
                "delivered_at": "2025-08-24T10:33:15Z",
                "read_at": "2025-08-24T10:45:30Z" if i % 3 == 0 else None,
                "response_received": i % 4 == 0
            }
            notifications.append(notification)
        
        return {
            "total_notifications": len(notifications),
            "filters_applied": {
                "alert_id": alert_id,
                "recipient_type": recipient_type
            },
            "notifications": notifications,
            "delivery_summary": {
                "delivered": len([n for n in notifications if n["delivery_status"] == "delivered"]),
                "pending": len([n for n in notifications if n["delivery_status"] == "pending"]),
                "failed": len([n for n in notifications if n["delivery_status"] == "failed"]),
                "read": len([n for n in notifications if n.get("read_at")])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get notification history: {str(e)}")

# Background task functions
async def send_alert_notifications(alert_record: Dict, targets: List[str]):
    """Background task to send alert notifications"""
    # Mock implementation - in production would send real notifications
    print(f"Sending notifications for alert {alert_record['alert_id']} to {targets}")

async def process_notifications(notification_record: Dict):
    """Background task to process and send notifications"""
    # Mock implementation
    print(f"Processing notification {notification_record['notification_id']}")

# Helper functions
def get_notification_contacts(recipient_type: str) -> List[Dict]:
    """Get contact information for different recipient types"""
    contact_database = {
        "authorities": [
            {"name": "Delhi Pollution Control Committee", "email": "alerts@dpcc.gov.in", "phone": "+91-11-2345-6789"},
            {"name": "Municipal Corporation", "email": "waste@mcd.gov.in", "phone": "+91-11-2345-6790"}
        ],
        "emergency": [
            {"name": "Emergency Response Team", "email": "emergency@satmap.org", "phone": "100"},
            {"name": "Health Emergency", "email": "health.emergency@gov.in", "phone": "102"}
        ],
        "community": [
            {"name": "Community WhatsApp Group", "contact": "+91-11-XXXX-XXXX"},
            {"name": "Local Newsletter", "email": "newsletter@community.org"}
        ]
    }
    
    return contact_database.get(recipient_type, [])

def generate_alert_recommendations(alert_type: str, priority: str) -> List[str]:
    """Generate recommendations based on alert type and priority"""
    recommendations = {
        "contamination": [
            "Isolate affected area immediately",
            "Deploy cleanup crew within 24 hours",
            "Monitor air and water quality",
            "Alert nearby residents"
        ],
        "health_risk": [
            "Issue public health advisory",
            "Provide medical screening for affected population",
            "Establish temporary medical facilities if needed",
            "Monitor disease surveillance systems"
        ],
        "cleanup_required": [
            "Schedule waste removal operations",
            "Coordinate with local waste management",
            "Arrange proper disposal facilities",
            "Document cleanup progress"
        ]
    }
    
    base_recommendations = recommendations.get(alert_type, ["Investigate and assess situation"])
    
    if priority == "critical":
        base_recommendations.insert(0, "IMMEDIATE ACTION REQUIRED")
    
    return base_recommendations

def generate_follow_up_actions(alert_type: str, priority: str) -> List[str]:
    """Generate follow-up actions"""
    actions = [
        "Monitor situation for 48 hours",
        "Collect follow-up environmental samples",
        "Document resolution status",
        "Update community on progress"
    ]
    
    if priority in ["critical", "high"]:
        actions.append("Schedule follow-up inspection within 1 week")
    
    return actions