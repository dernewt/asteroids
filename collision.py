import pygame

class Collision:
    @staticmethod
    def circle_line_collision(circle_center, circle_radius, pt1, pt2):
        cx, cy = circle_center
        ax, ay = pt1
        bx, by = pt2

        abx = bx - ax
        aby = by - ay
        acx = cx - ax
        acy = cy - ay

        ab_len_sq = (abx * abx) + (aby * aby)
        if ab_len_sq == 0:
            # A and B are the same point
            closest_x, closest_y = ax, ay

        else:
            # Project point onto the segment.
            t = max(0, min(1, (acx * abx + acy * aby)/ ab_len_sq))
            closest_x = ax + t * abx
            closest_y = ay + t * aby

        dx = cx - closest_x
        dy = cy - closest_y
        return dx**2 + dy**2 <= circle_radius**2


    @staticmethod
    def circle_triangle_collision(circle_center, circle_radius, a, b, c):
        return (
            Collision.circle_line_collision(circle_center, circle_radius, a, b)
            or Collision.circle_line_collision(circle_center, circle_radius, a, c)
            or Collision.circle_line_collision(circle_center, circle_radius, b, c)
            )
