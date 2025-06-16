# main.py

from business.circle_detector import CircleDetector
from business.robot_detector import RobotDetector
from services.image_processing_service import ImageProcessingService
from ui.image_adjustment_ui import ImageAdjustmentUI

if __name__ == "__main__":
    circle_detector = CircleDetector()
    robot_detector = RobotDetector()
    service = ImageProcessingService(circle_detector, robot_detector)
    app = ImageAdjustmentUI(service)
    app.root.mainloop()
