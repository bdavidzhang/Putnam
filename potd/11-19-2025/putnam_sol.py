from manim import *
import numpy as np

class TheControlPanel(Scene):
    def construct(self):
        self.intro_flattening()
        self.lazy_river_analogy()
        self.parity_check()

    def intro_flattening(self):
        # 1. Create the 2D Schlegel Diagram of a Dodecahedron
        # (This represents looking top-down at the "City of Pipes")
        
        # Define vertices for a simplified Schlegel projection (2 rings of 5 + center/outer)
        # This is a topological approximation for clarity
        outer_ring = [np.array([3*np.cos(theta), 3*np.sin(theta), 0]) 
                      for theta in np.linspace(0, 2*np.pi, 5, endpoint=False)]
        mid_ring = [np.array([1.5*np.cos(theta + np.pi/5), 1.5*np.sin(theta + np.pi/5), 0]) 
                    for theta in np.linspace(0, 2*np.pi, 5, endpoint=False)]
        inner_ring = [np.array([0.7*np.cos(theta), 0.7*np.sin(theta), 0]) 
                      for theta in np.linspace(0, 2*np.pi, 5, endpoint=False)]
        
        # Create dots
        dots = VGroup(*[Dot(p) for p in outer_ring + mid_ring + inner_ring])
        
        # Create edges (simplified connectivity for visual demonstration of loops)
        edges = VGroup()
        # Connect rings logic would go here, but for the narrative, 
        # we will visually highlight the "Windows" (Faces) directly.
        
        title = Text("The Control Panel", font_size=40).to_edge(UP)
        subtitle = Text("Flattening the Dodecahedron", font_size=24).next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        
        # Draw the "Mesh"
        # We draw a graph that looks like the Schlegel diagram
        graph_config = {
            "vertex_config": {"radius": 0.08, "color": WHITE},
            "edge_config": {"stroke_color": BLUE, "stroke_width": 4}
        }
        # Defining a dodecahedral graph layout manually is verbose, 
        # so we use a DodecahedralGraph class from NetworkX or simulate the layout.
        # Here we draw the critical visual: The Pentagonal Faces (Loops)
        
        self.play(Create(dots))
        
        instruction = Text("Every 'Window' is a Knob", color=YELLOW, font_size=32).to_edge(DOWN)
        self.play(Write(instruction))
        self.wait(1)
        
        # Clean up for next section
        self.dots = dots # Save for reference
        self.title = title
        self.instruction = instruction
        self.play(FadeOut(subtitle))

    def lazy_river_analogy(self):
        # 2. The Lazy River (Kernel)
        
        # Focus on one specific pentagonal loop (Cycle)
        loop_points = [
            np.array([0, 1.5, 0]),
            np.array([-1.4, 0.5, 0]),
            np.array([-0.9, -1, 0]),
            np.array([0.9, -1, 0]),
            np.array([1.4, 0.5, 0]),
            np.array([0, 1.5, 0]) # close loop
        ]
        
        lazy_river = VMobject()
        lazy_river.set_points_as_corners(loop_points)
        lazy_river.set_color(YELLOW).set_stroke(width=8)
        
        label = Text("The Lazy River (+1 flow)", font_size=24, color=YELLOW).move_to(UP*2)
        
        self.play(Transform(self.instruction, label))
        self.play(Create(lazy_river))
        
        # Animate flow along the river
        # Create small arrows moving along the path
        arrows = VGroup(*[Arrow(start=loop_points[i], end=loop_points[i+1], buff=0, color=YELLOW).scale(0.5) 
                          for i in range(5)])
        
        self.play(FadeIn(arrows))
        
        # Show Vertex Sum Check
        # Pick one vertex on the loop
        v_point = loop_points[1]
        focus_circle = Circle(radius=0.3, color=RED).move_to(v_point)
        
        check_text = MathTex(r"\text{In} +1, \text{Out} +1 \implies \Delta = 0").next_to(focus_circle, LEFT).scale(0.8)
        
        self.play(Create(focus_circle))
        self.play(Write(check_text))
        self.wait(2)
        
        # Count the loops
        count_text = Text("11 Independent Loops", font_size=36).move_to(DOWN*2)
        math_text = MathTex(r"\text{Choices} = 3^{11}").next_to(count_text, DOWN)
        
        self.play(FadeOut(lazy_river), FadeOut(arrows), FadeOut(focus_circle), FadeOut(check_text))
        self.play(Write(count_text), Write(math_text))
        self.wait(2)
        
        self.play(FadeOut(count_text), FadeOut(math_text), FadeOut(self.dots))

    def parity_check(self):
        # 3. The Global Parity (Flux)
        
        new_title = Text("The Global Parity Law", font_size=36).to_edge(UP)
        self.play(Transform(self.title, new_title), FadeOut(self.instruction))
        
        # Create a grid of 20 vertices
        vertices = VGroup(*[Dot(radius=0.15, color=GREY) for _ in range(20)]).arrange_in_grid(4, 5, buff=0.8)
        self.play(Create(vertices))
        
        # Randomly assign valid flux (Green) to the first 19
        valid_group = vertices[:19]
        self.play(valid_group.animate.set_color(GREEN), run_time=1.5)
        
        txt = Text("19 Choices: Anything goes", font_size=24, color=GREEN).next_to(vertices, DOWN)
        self.play(Write(txt))
        
        # The last vertex (The 20th)
        last_vertex = vertices[19]
        arrow = Arrow(start=RIGHT, end=LEFT, color=RED).next_to(last_vertex, RIGHT)
        warning = Text("Must balance the universe!", font_size=20, color=RED).next_to(arrow, RIGHT)
        
        self.play(Create(arrow), Write(warning))
        
        # Flash the last vertex
        self.play(last_vertex.animate.set_color(RED).scale(1.5))
        self.play(last_vertex.animate.scale(1/1.5))
        
        # Final Formula
        final_formula = MathTex(r"\text{Total} = \frac{2^{20}}{3} \times 3^{11}").scale(1.5)
        background_rect = SurroundingRectangle(final_formula, color=BLACK, fill_opacity=0.8)
        
        self.play(
            FadeIn(background_rect),
            Write(final_formula)
        )
        self.wait(3)