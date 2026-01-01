from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import json
from .models import meeting_manager


@login_required
@require_http_methods(["GET", "POST"])
def meeting_list_create(request):
    """List all meetings or create a new meeting"""
    
    # IMPORTANT: Ensure user_id is a string to match MongoDB storage
    user_id_str = str(request.user.id)

    if request.method == "GET":
        try:
            # Pass the string version of ID
            meetings = meeting_manager.get_user_meetings(user_id_str)
            
            now = datetime.utcnow()
            for meeting in meetings:
                try:
                    # Fix: Handle both YYYY-MM-DD and other potential formats
                    m_date = meeting.get('meeting_date')
                    m_time = meeting.get('meeting_time')
                    
                    if m_date and m_time:
                        meeting_datetime = datetime.strptime(
                            f"{m_date} {m_time}", 
                            '%Y-%m-%d %H:%M'
                        )
                        meeting['is_past'] = meeting_datetime < now
                        # Upcoming = within the next 24 hours
                        meeting['is_upcoming'] = now < meeting_datetime < now + timedelta(days=1)
                    else:
                        meeting['is_past'] = False
                        meeting['is_upcoming'] = False
                except Exception:
                    meeting['is_past'] = False
                    meeting['is_upcoming'] = False
            
            return JsonResponse({'meetings': meetings})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # 1. Validation
            required_fields = ['title', 'meeting_date', 'meeting_time']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'error': f'{field} is required'}, status=400)
            
            # 2. Date/Time format validation
            try:
                # We validate format but keep them as strings for MongoDB
                meeting_date_obj = datetime.strptime(data['meeting_date'], '%Y-%m-%d')
                meeting_time_obj = datetime.strptime(data['meeting_time'], '%H:%M')
            except ValueError:
                return JsonResponse({'error': 'Invalid date or time format. Use YYYY-MM-DD and HH:MM'}, status=400)
            
            # 3. Prevent past meetings (Logic Fix)
            # Use datetime.now() for local comparison or utcnow() to match your storage
            meeting_datetime = datetime.combine(meeting_date_obj.date(), meeting_time_obj.time())
            if meeting_datetime < datetime.now():
                return JsonResponse({'error': 'Cannot create meeting in the past'}, status=400)
            
            # 4. Create meeting using the string ID
            meeting = meeting_manager.create_meeting(user_id_str, data)
            
            return JsonResponse({
                'message': 'Meeting created successfully',
                'meeting': meeting
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Failed to create meeting: {str(e)}'}, status=500)
    """List all meetings or create a new meeting"""
    
    if request.method == "GET":
        try:
            meetings = meeting_manager.get_user_meetings(request.user.id)
            
            # Add computed fields
            now = datetime.utcnow()
            for meeting in meetings:
                try:
                    meeting_datetime = datetime.strptime(
                        f"{meeting['meeting_date']} {meeting['meeting_time']}", 
                        '%Y-%m-%d %H:%M'
                    )
                    meeting['is_past'] = meeting_datetime < now
                    meeting['is_upcoming'] = now < meeting_datetime < now + timedelta(days=1)
                except:
                    meeting['is_past'] = False
                    meeting['is_upcoming'] = False
            
            return JsonResponse({'meetings': meetings})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['title', 'meeting_date', 'meeting_time']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'error': f'{field} is required'}, status=400)
            
            # Validate date format
            try:
                meeting_date = datetime.strptime(data['meeting_date'], '%Y-%m-%d')
                meeting_time = datetime.strptime(data['meeting_time'], '%H:%M')
            except ValueError:
                return JsonResponse({'error': 'Invalid date or time format'}, status=400)
            
            # Check if meeting is in the past
            meeting_datetime = datetime.combine(meeting_date.date(), meeting_time.time())
            if meeting_datetime < datetime.now():
                return JsonResponse({'error': 'Cannot create meeting in the past'}, status=400)
            
            # Create meeting
            meeting = meeting_manager.create_meeting(request.user.id, data)
            
            return JsonResponse({
                'message': 'Meeting created successfully',
                'meeting': meeting
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Failed to create meeting: {str(e)}'}, status=500)


@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def meeting_detail(request, meeting_id):
    """Get, update, or delete a specific meeting"""
    
    if request.method == "GET":
        try:
            meeting = meeting_manager.get_meeting_by_id(meeting_id, request.user.id)
            if not meeting:
                return JsonResponse({'error': 'Meeting not found'}, status=404)
            
            return JsonResponse({'meeting': meeting})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            
            # Validate date/time formats if provided
            if 'meeting_date' in data:
                try:
                    datetime.strptime(data['meeting_date'], '%Y-%m-%d')
                except ValueError:
                    return JsonResponse({'error': 'Invalid date format'}, status=400)
            
            if 'meeting_time' in data:
                try:
                    datetime.strptime(data['meeting_time'], '%H:%M')
                except ValueError:
                    return JsonResponse({'error': 'Invalid time format'}, status=400)
            
            # Update meeting
            success = meeting_manager.update_meeting(meeting_id, request.user.id, data)
            
            if not success:
                return JsonResponse({'error': 'Meeting not found or update failed'}, status=404)
            
            # Get updated meeting
            meeting = meeting_manager.get_meeting_by_id(meeting_id, request.user.id)
            
            return JsonResponse({
                'message': 'Meeting updated successfully',
                'meeting': meeting
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Failed to update meeting: {str(e)}'}, status=500)
    
    elif request.method == "DELETE":
        try:
            success = meeting_manager.delete_meeting(meeting_id, request.user.id)
            
            if not success:
                return JsonResponse({'error': 'Meeting not found or delete failed'}, status=404)
            
            return JsonResponse({'message': 'Meeting deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)