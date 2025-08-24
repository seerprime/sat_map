import cv2
import numpy as np
import random
from typing import List, Dict, Tuple
from PIL import Image
import io
import base64

class TrashDetector:
    def __init__(self):
        self.trash_types = [
            "plastic_bottle", "plastic_bag", "food_wrapper", 
            "cigarette_butt", "aluminum_can", "glass_bottle",
            "paper_cup", "cardboard", "organic_waste", "electronics"
        ]
        
        self.recycling_info = {
            "plastic_bottle": {
                "recyclable": True,
                "bin": "plastic_recycling",
                "tip": "Remove cap and rinse before recycling"
            },
            "plastic_bag": {
                "recyclable": False,
                "bin": "general_waste", 
                "tip": "Take to grocery store plastic bag recycling"
            },
            "food_wrapper": {
                "recyclable": False,
                "bin": "general_waste",
                "tip": "Most food wrappers are not recyclable"
            },
            "cigarette_butt": {
                "recyclable": False,
                "bin": "general_waste",
                "tip": "Cigarette butts are toxic waste - dispose properly"
            },
            "aluminum_can": {
                "recyclable": True,
                "bin": "metal_recycling", 
                "tip": "Rinse and crush to save space"
            },
            "glass_bottle": {
                "recyclable": True,
                "bin": "glass_recycling",
                "tip": "Remove caps and rinse before recycling"
            },
            "paper_cup": {
                "recyclable": False,
                "bin": "general_waste",
                "tip": "Plastic lining makes most paper cups non-recyclable"
            },
            "cardboard": {
                "recyclable": True,
                "bin": "paper_recycling",
                "tip": "Remove tape and flatten boxes"
            },
            "organic_waste": {
                "recyclable": False,
                "bin": "compost",
                "tip": "Perfect for composting - turn into soil!"
            },
            "electronics": {
                "recyclable": True,
                "bin": "e_waste",
                "tip": "Take to certified e-waste recycling center"
            }
        }
    
    def detect_trash(self, image_data: bytes) -> Dict:
        """
        Mock YOLO detection that analyzes image and returns realistic trash detection results
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to OpenCV format for analysis
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            height, width = cv_image.shape[:2]
            
            # Analyze image characteristics for realistic detection
            detections = self._analyze_image_for_trash(cv_image, width, height)
            
            # Calculate overall metrics
            total_items = len(detections)
            avg_confidence = sum(d['confidence'] for d in detections) / max(1, total_items)
            estimated_weight = sum(d['estimated_weight'] for d in detections)
            
            return {
                "success": True,
                "total_items_detected": total_items,
                "average_confidence": round(avg_confidence, 3),
                "estimated_total_weight_kg": round(estimated_weight, 2),
                "detections": detections,
                "processing_time_ms": random.randint(800, 1500),
                "model_version": "YOLOv8-SatMap-v1.2"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "detections": []
            }
    
    def _analyze_image_for_trash(self, image: np.ndarray, width: int, height: int) -> List[Dict]:
        """
        Analyze image characteristics to generate realistic trash detections
        """
        detections = []
        
        # Calculate image complexity metrics
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (width * height)
        
        # Color analysis for trash likelihood
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Generate realistic number of detections based on image characteristics
        base_detections = 0
        if edge_density > 0.1:  # Complex scene
            base_detections = random.randint(2, 8)
        elif edge_density > 0.05:  # Moderate complexity
            base_detections = random.randint(1, 4)
        else:  # Simple scene
            base_detections = random.randint(0, 2)
        
        # Generate detections
        for i in range(base_detections):
            trash_type = random.choice(self.trash_types)
            
            # Generate realistic bounding box
            x1 = random.randint(0, width - 100)
            y1 = random.randint(0, height - 100)
            box_width = random.randint(50, min(200, width - x1))
            box_height = random.randint(50, min(200, height - y1))
            
            # Calculate confidence based on "detection quality"
            confidence = self._calculate_confidence(trash_type, box_width, box_height)
            
            detection = {
                "type": trash_type,
                "confidence": confidence,
                "bounding_box": {
                    "x1": x1,
                    "y1": y1, 
                    "x2": x1 + box_width,
                    "y2": y1 + box_height,
                    "width": box_width,
                    "height": box_height
                },
                "estimated_weight": self._estimate_weight(trash_type, box_width, box_height),
                "recyclable": self.recycling_info[trash_type]["recyclable"],
                "recycling_tip": self.recycling_info[trash_type]["tip"]
            }
            
            detections.append(detection)
        
        return detections
    
    def _calculate_confidence(self, trash_type: str, width: int, height: int) -> float:
        """Calculate realistic confidence score"""
        base_confidence = {
            "plastic_bottle": 0.85,
            "aluminum_can": 0.82,
            "glass_bottle": 0.78,
            "plastic_bag": 0.65,
            "food_wrapper": 0.72,
            "cigarette_butt": 0.68,
            "paper_cup": 0.75,
            "cardboard": 0.80,
            "organic_waste": 0.60,
            "electronics": 0.88
        }
        
        confidence = base_confidence.get(trash_type, 0.7)
        
        # Adjust based on size (larger objects = higher confidence)
        size_factor = min(1.0, (width * height) / 10000)
        confidence += size_factor * 0.1
        
        # Add some randomness
        confidence += random.uniform(-0.05, 0.05)
        
        return max(0.3, min(0.95, round(confidence, 3)))
    
    def _estimate_weight(self, trash_type: str, width: int, height: int) -> float:
        """Estimate weight based on trash type and size"""
        weight_per_pixel = {
            "plastic_bottle": 0.00008,
            "aluminum_can": 0.00005,  
            "glass_bottle": 0.0002,
            "plastic_bag": 0.00001,
            "food_wrapper": 0.00002,
            "cigarette_butt": 0.000005,
            "paper_cup": 0.00003,
            "cardboard": 0.00004,
            "organic_waste": 0.0001,
            "electronics": 0.0005
        }
        
        area = width * height
        base_weight = area * weight_per_pixel.get(trash_type, 0.00005)
        
        # Add randomness
        weight = base_weight * random.uniform(0.7, 1.3)
        
        return round(weight, 4)
    
    def get_trash_categories(self) -> List[str]:
        """Return list of detectable trash categories"""
        return self.trash_types
    
    def get_recycling_info(self, trash_type: str) -> Dict:
        """Get recycling information for specific trash type"""
        return self.recycling_info.get(trash_type, {
            "recyclable": False,
            "bin": "general_waste", 
            "tip": "Check with local recycling guidelines"
        })