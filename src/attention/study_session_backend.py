import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable
from precise_attention_tracker import PreciseAttentionTracker

class StudySessionBackend:
    """
    Backend for managing study sessions with attention tracking.
    Integrates with existing Study Spark UI.
    """
    
    def __init__(self):
        self.current_session = None
        self.session_timer = None
        self.attention_tracker = None
        self.session_data = {
            "session_type": None,
            "start_time": None,
            "end_time": None,
            "current_phase": None,  # "focus", "break", "long_break"
            "rounds_completed": 0,
            "total_focus_time": 0,
            "total_break_time": 0,
            "phone_detections": 0,
            "focus_score_avg": 0.0,
            "is_active": False
        }
        
    def start_pomodoro_session(self, rounds: int = 4) -> Dict[str, Any]:
        """Start Pomodoro session: 25 min focus, 5 min break, longer break every 4 rounds"""
        session_config = {
            "type": "pomodoro",
            "focus_duration": 25 * 60,  # 25 minutes in seconds
            "break_duration": 5 * 60,    # 5 minutes in seconds
            "long_break_duration": 15 * 60,  # 15 minutes in seconds
            "rounds": rounds,
            "current_round": 0
        }
        return self._start_session(session_config)
    
    def start_52_17_session(self) -> Dict[str, Any]:
        """Start 52/17 session: 52 min work, 17 min break"""
        session_config = {
            "type": "52_17",
            "focus_duration": 52 * 60,   # 52 minutes in seconds
            "break_duration": 17 * 60,   # 17 minutes in seconds
            "rounds": 1,
            "current_round": 0
        }
        return self._start_session(session_config)
    
    def start_deep_work_session(self) -> Dict[str, Any]:
        """Start Deep Work session: 90 min focus, 20 min rest"""
        session_config = {
            "type": "deep_work",
            "focus_duration": 90 * 60,   # 90 minutes in seconds
            "break_duration": 20 * 60,  # 20 minutes in seconds
            "rounds": 1,
            "current_round": 0
        }
        return self._start_session(session_config)
    
    def start_phone_free_sprint(self, duration_minutes: int = 30) -> Dict[str, Any]:
        """Start Phone-Free Sprint: configurable duration with phone detection"""
        session_config = {
            "type": "phone_free_sprint",
            "focus_duration": duration_minutes * 60,  # Convert to seconds
            "break_duration": 0,  # No breaks in sprint
            "rounds": 1,
            "current_round": 0
        }
        return self._start_session(session_config)
    
    def _start_session(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method to start any study session"""
        if self.session_data["is_active"]:
            return {"error": "Session already active", "status": "error"}
        
        # Initialize session
        self.current_session = config
        self.session_data.update({
            "session_type": config["type"],
            "start_time": datetime.now(),
            "current_phase": "focus",
            "rounds_completed": 0,
            "total_focus_time": 0,
            "total_break_time": 0,
            "phone_detections": 0,
            "focus_score_avg": 0.0,
            "is_active": True
        })
        
        # Start attention tracker with 1280x720 resolution
        self.attention_tracker = PreciseAttentionTracker(frame_width=1280, frame_height=720)
        
        # Start session timer
        self._start_session_timer()
        
        return {
            "status": "started",
            "session_type": config["type"],
            "duration": config["focus_duration"],
            "phase": "focus"
        }
    
    def _start_session_timer(self):
        """Start the session timer thread"""
        self.session_timer = threading.Thread(target=self._run_session_timer)
        self.session_timer.daemon = True
        self.session_timer.start()
    
    def _run_session_timer(self):
        """Main session timer loop"""
        while self.session_data["is_active"] and self.current_session:
            current_phase = self.session_data["current_phase"]
            session_type = self.current_session["type"]
            
            if current_phase == "focus":
                duration = self.current_session["focus_duration"]
                self._run_focus_phase(duration)
            elif current_phase == "break":
                duration = self.current_session["break_duration"]
                self._run_break_phase(duration)
            elif current_phase == "long_break":
                duration = self.current_session.get("long_break_duration", self.current_session["break_duration"])
                self._run_break_phase(duration)
            
            # Check if session should continue
            if not self._should_continue_session():
                break
    
    def _run_focus_phase(self, duration_seconds: int):
        """Run focus phase with attention tracking"""
        print(f"🎯 FOCUS PHASE: {duration_seconds//60} minutes")
        start_time = time.time()
        
        # Start attention tracker
        if self.attention_tracker:
            # Run attention tracker for the focus duration
            self._run_attention_tracking(duration_seconds)
        
        # Update session data
        actual_duration = time.time() - start_time
        self.session_data["total_focus_time"] += actual_duration
        self.session_data["rounds_completed"] += 1
        
        # Move to break phase (except for phone-free sprint)
        if self.current_session["type"] != "phone_free_sprint":
            self.session_data["current_phase"] = "break"
        else:
            # Phone-free sprint ends after focus phase
            self._end_session()
    
    def _run_break_phase(self, duration_seconds: int):
        """Run break phase"""
        print(f"☕ BREAK PHASE: {duration_seconds//60} minutes")
        
        # Stop attention tracker during break
        if self.attention_tracker:
            # Could implement break-specific tracking here
            pass
        
        time.sleep(duration_seconds)
        
        # Update session data
        self.session_data["total_break_time"] += duration_seconds
        
        # Check if we need a long break (Pomodoro only)
        if (self.current_session["type"] == "pomodoro" and 
            self.session_data["rounds_completed"] % 4 == 0):
            self.session_data["current_phase"] = "long_break"
        else:
            self.session_data["current_phase"] = "focus"
    
    def _run_attention_tracking(self, duration_seconds: int):
        """Run attention tracker for specified duration"""
        if not self.attention_tracker:
            return
        
        start_time = time.time()
        focus_scores = []
        phone_detections = 0
        
        print(f"📊 Starting attention tracking for {duration_seconds//60} minutes...")
        
        # Run attention tracker for the duration
        while time.time() - start_time < duration_seconds:
            try:
                # Get attention metrics
                metrics = self.attention_tracker.process_frame(self.attention_tracker.cap.read()[1])
                
                # Track focus score
                focus_score = metrics.get("focus_score", 0.0)
                focus_scores.append(focus_score)
                
                # Track phone detections
                if metrics.get("phone_near_face", False) or metrics.get("ai_detected_phone", False):
                    phone_detections += 1
                    print("📱 Phone detected!")
                
                # Update session data
                self.session_data["phone_detections"] += phone_detections
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Attention tracking error: {e}")
                break
        
        # Calculate average focus score
        if focus_scores:
            self.session_data["focus_score_avg"] = sum(focus_scores) / len(focus_scores)
        
        print(f"📈 Session stats - Focus avg: {self.session_data['focus_score_avg']:.2f}, Phone detections: {phone_detections}")
    
    def _should_continue_session(self) -> bool:
        """Check if session should continue"""
        if not self.current_session:
            return False
        
        session_type = self.current_session["type"]
        rounds_completed = self.session_data["rounds_completed"]
        total_rounds = self.current_session["rounds"]
        
        # Check if we've completed all rounds
        if rounds_completed >= total_rounds:
            return False
        
        return True
    
    def pause_session(self) -> Dict[str, Any]:
        """Pause the current session"""
        if not self.session_data["is_active"]:
            return {"error": "No active session", "status": "error"}
        
        self.session_data["is_active"] = False
        return {"status": "paused", "session_type": self.session_data["session_type"]}
    
    def resume_session(self) -> Dict[str, Any]:
        """Resume the paused session"""
        if self.session_data["is_active"]:
            return {"error": "Session already active", "status": "error"}
        
        self.session_data["is_active"] = True
        self._start_session_timer()
        return {"status": "resumed", "session_type": self.session_data["session_type"]}
    
    def end_session(self) -> Dict[str, Any]:
        """End the current session"""
        return self._end_session()
    
    def _end_session(self) -> Dict[str, Any]:
        """Internal method to end session"""
        if not self.session_data["is_active"]:
            return {"error": "No active session", "status": "error"}
        
        self.session_data.update({
            "is_active": False,
            "end_time": datetime.now()
        })
        
        # Stop attention tracker
        if self.attention_tracker:
            self.attention_tracker.cap.release()
            self.attention_tracker = None
        
        # Calculate session summary
        session_summary = self._get_session_summary()
        
        return {
            "status": "completed",
            "session_type": self.session_data["session_type"],
            "summary": session_summary
        }
    
    def _get_session_summary(self) -> Dict[str, Any]:
        """Get session summary statistics"""
        if self.session_data["start_time"] and self.session_data["end_time"]:
            total_duration = (self.session_data["end_time"] - self.session_data["start_time"]).total_seconds()
        else:
            total_duration = 0
        
        return {
            "total_duration_minutes": total_duration / 60,
            "focus_time_minutes": self.session_data["total_focus_time"] / 60,
            "break_time_minutes": self.session_data["total_break_time"] / 60,
            "rounds_completed": self.session_data["rounds_completed"],
            "phone_detections": self.session_data["phone_detections"],
            "average_focus_score": self.session_data["focus_score_avg"],
            "focus_percentage": (self.session_data["total_focus_time"] / total_duration * 100) if total_duration > 0 else 0
        }
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        return {
            "is_active": self.session_data["is_active"],
            "session_type": self.session_data["session_type"],
            "current_phase": self.session_data["current_phase"],
            "rounds_completed": self.session_data["rounds_completed"],
            "phone_detections": self.session_data["phone_detections"],
            "focus_score_avg": self.session_data["focus_score_avg"]
        }

# Example usage and API endpoints
def create_study_session_api():
    """Create API endpoints for study session management"""
    session_backend = StudySessionBackend()
    
    def start_pomodoro():
        return session_backend.start_pomodoro_session()
    
    def start_52_17():
        return session_backend.start_52_17_session()
    
    def start_deep_work():
        return session_backend.start_deep_work_session()
    
    def start_phone_free_sprint(duration=30):
        return session_backend.start_phone_free_sprint(duration)
    
    def pause_session():
        return session_backend.pause_session()
    
    def resume_session():
        return session_backend.resume_session()
    
    def end_session():
        return session_backend.end_session()
    
    def get_status():
        return session_backend.get_session_status()
    
    return {
        "start_pomodoro": start_pomodoro,
        "start_52_17": start_52_17,
        "start_deep_work": start_deep_work,
        "start_phone_free_sprint": start_phone_free_sprint,
        "pause_session": pause_session,
        "resume_session": resume_session,
        "end_session": end_session,
        "get_status": get_status
    }

if __name__ == "__main__":
    # Test the study session backend
    print("🧠 Study Session Backend - Test Mode")
    print("Available study techniques:")
    print("1. Pomodoro: 25 min focus + 5 min break")
    print("2. 52/17: 52 min work + 17 min break") 
    print("3. Deep Work: 90 min focus + 20 min rest")
    print("4. Phone-Free Sprint: configurable duration")
    
    # Create API
    api = create_study_session_api()
    
    # Example: Start a short Pomodoro session for testing
    print("\n🎯 Starting test Pomodoro session (1 minute focus, 30 second break)...")
    
    # Override for testing
    session_backend = StudySessionBackend()
    session_backend.current_session = {
        "type": "pomodoro",
        "focus_duration": 60,  # 1 minute for testing
        "break_duration": 30,   # 30 seconds for testing
        "long_break_duration": 60,
        "rounds": 2,
        "current_round": 0
    }
    
    result = session_backend._start_session(session_backend.current_session)
    print(f"Session started: {result}")
    
    # Let it run for a bit
    time.sleep(5)
    
    # Get status
    status = session_backend.get_session_status()
    print(f"Session status: {status}")
    
    # End session
    result = session_backend.end_session()
    print(f"Session ended: {result}")
