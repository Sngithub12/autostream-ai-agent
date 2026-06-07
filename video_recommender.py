"""
Video content recommendations based on user intent
"""
import json
import os
from typing import List, Dict

class VideoRecommender:
    def __init__(self):
        self.videos = self._load_videos()
    
    def _load_videos(self) -> Dict:
        """Load video recommendations from JSON"""
        try:
            with open('data/videos.json', 'r') as f:
                return json.load(f)
        except:
            return self._default_videos()
    
    def _default_videos(self) -> Dict:
        return {
            "pricing": {
                "title": "Pricing Overview",
                "url": "https://youtube.com/embed/example1",
                "duration": "5 min"
            },
            "features": {
                "title": "Feature Walkthrough",
                "url": "https://youtube.com/embed/example2",
                "duration": "10 min"
            },
            "setup": {
                "title": "Getting Started",
                "url": "https://youtube.com/embed/example3",
                "duration": "8 min"
            },
            "demo": {
                "title": "Live Demo",
                "url": "https://youtube.com/embed/example4",
                "duration": "15 min"
            }
        }
    
    def get_recommendation(self, intent: str) -> Dict:
        """Get video recommendation based on intent"""
        intent_to_video = {
            "pricing": "pricing",
            "features": "features",
            "demo": "demo",
            "setup": "setup"
        }
        
        video_key = intent_to_video.get(intent, "demo")
        return self.videos.get(video_key, {})
    
    def get_all_videos(self) -> List[Dict]:
        """Get all available videos"""
        return list(self.videos.values())
