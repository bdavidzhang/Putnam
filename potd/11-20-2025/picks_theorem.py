from manim import *

class PicksTheorem(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        # Define a polygon with integer coordinates
        # Let's use a triangle for simplicity and clarity: (0,0), (4,0), (0,3)
        # This is a 3-4-5 triangle. Area should be 6.
        vertices = [
            [0, 0, 0],
            [4, 0, 0],
            [0, 3, 0]
        ]
        
        # Coordinates of Lattice Points (Hardcoded for this specific shape for precision)
        # Boundary Points (On the edges)
        boundary_coords = [
            [0,0,0], [1,0,0], [2,0,0], [3,0,0], [4,0,0], # Bottom edge
            [0,1,0], [0,2,0], [0,3,0]                    # Left edge
            # Hypotenuse of 3-4-5 triangle has no integer points strictly between endpoints
        ]
        
        # Interior Points (Inside the shape)
        # Inside x=1: (1,1), (1,2)
        # Inside x=2: (2,1)
        interior_coords = [
            [1,1,0], [1,2,0], [2,1,0]
        ]
        
        num_boundary = len(boundary_coords) # Should be 8
        num_interior = len(interior_coords) # Should be 3
        
        # --- ANIMATION START ---
        
        # 1. Setup Grid
        plane = NumberPlane(
            x_range=[-1, 6, 1],
            y_range=[-1, 5, 1],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )
        self.play(Create(plane), run_time=2)
        
        # 2. Draw Polygon
        polygon = Polygon(*vertices, color=WHITE, stroke_width=4)
        polygon.set_fill(BLUE, opacity=0.2)
        
        label_poly = Text("Polygon P", font_size=24).move_to(polygon.get_center())
        
        self.play(DrawBorderThenFill(polygon), Write(label_poly))
        self.wait(1)
        
        # 3. Explain Pick's Theorem Formula
        formula = MathTex(
            r"\text{Area} =", r"I", r"+", r"\frac{B}{2}", r"- 1"
        ).to_edge(UP).shift(LEFT * 1)
        
        formula[1].set_color(YELLOW) # I color
        formula[3].set_color(TEAL)   # B color
        
        title = Text("Pick's Theorem", font_size=36).next_to(formula, UP)
        
        self.play(Write(title), Write(formula))
        self.wait(1)
        
        # 4. Visualizing Boundary Points (B)
        b_dots = VGroup()
        for coord in boundary_coords:
            dot = Dot(point=coord, color=TEAL, radius=0.12)
            dot.set_stroke(BLACK, width=1)
            b_dots.add(dot)
            
        b_label = MathTex(r"B =", str(num_boundary), color=TEAL).next_to(polygon, RIGHT, buff=1).shift(UP)
        
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in b_dots], lag_ratio=0.1),
            run_time=1.5
        )
        self.play(Write(b_label))
        
        # 5. Visualizing Interior Points (I)
        i_dots = VGroup()
        for coord in interior_coords:
            dot = Dot(point=coord, color=YELLOW, radius=0.12)
            dot.set_stroke(BLACK, width=1)
            i_dots.add(dot)
            
        i_label = MathTex(r"I =", str(num_interior), color=YELLOW).next_to(b_label, DOWN, buff=0.5)
        
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in i_dots], lag_ratio=0.1),
            run_time=1.5
        )
        self.play(Write(i_label))
        self.wait(1)
        
        # 6. Calculation Substitution
        calc_step1 = MathTex(
            r"\text{Area} =", str(num_interior), r"+", r"\frac{" + str(num_boundary) + r"}{2}", r"- 1"
        ).next_to(formula, DOWN, buff=0.5).align_to(formula, LEFT)
        
        # Color matching
        calc_step1[1].set_color(YELLOW)
        calc_step1[3].set_color(TEAL)

        calc_step2 = MathTex(
            r"\text{Area} =", str(num_interior), r"+", str(int(num_boundary/2)), r"- 1"
        ).next_to(calc_step1, DOWN).align_to(calc_step1, LEFT)
        
        final_area = num_interior + (num_boundary / 2) - 1
        calc_step3 = MathTex(
            r"\text{Area} =", str(int(final_area))
        ).next_to(calc_step2, DOWN).align_to(calc_step2, LEFT)
        calc_step3.set_color(GREEN)

        self.play(TransformFromCopy(formula, calc_step1))
        self.wait(1)
        self.play(ReplacementTransform(calc_step1, calc_step2))
        self.wait(1)
        self.play(ReplacementTransform(calc_step2, calc_step3))
        self.play(Indicate(calc_step3))
        
        # 7. Conclusion / Verification
        # Show standard geometry calculation (Base * Height / 2)
        verification = MathTex(r"\text{Geometry Check: } \frac{4 \times 3}{2} = 6").to_edge(DOWN)
        self.play(Write(verification))
        
        self.wait(3)