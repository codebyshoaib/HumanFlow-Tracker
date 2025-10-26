import math

class Tracker:
    def __init__(self, distance_threshold=25):
        self.center_points = {}  # {id: (cx, cy)}
        self.id_count = 0
        self.distance_threshold = distance_threshold

    def update(self, object_rects):
        objects_bbs_ids = []

        # New centers this frame
        new_center_points = {}

        for rect in object_rects:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            matched = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < self.distance_threshold:
                    new_center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    matched = True
                    break

            if not matched:
                # New object
                new_center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        self.center_points = new_center_points.copy()
        return objects_bbs_ids
