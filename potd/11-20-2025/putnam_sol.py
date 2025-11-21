from manim import *


class PutnamA3Problem(Scene):
    def construct(self):
        # --- Slide 3: Problem Statement ---
        problem_text_en = Text(
            "Prove that any convex pentagon whose vertices (no three of which are collinear)\n"
            "have integer coordinates must have area greater than or equal to 5/2.",
            font_size=24,
            line_spacing=1.5,
            t2c={"convex pentagon": BLUE, "integer coordinates": YELLOW, "area greater than or equal to 5/2": RED}
        ).to_edge(UP, buff=1)
        
        # Note: Rendering Chinese characters requires a compatible font to be available on the system.
        # Manim will try to find a fallback font if the default doesn't work.
        problem_text_cn = Text(
            "证明：任何凸五边形，定点全部为整数，面积必定大于等于5/2。",
            font_size=32
        ).next_to(problem_text_en, DOWN, buff=1.5)

        problem_group = VGroup(problem_text_en, problem_text_cn)

        self.play(Write(problem_group), run_time=3)
        
        # **Crucial**: Add time for the viewer to think about the problem as requested.
        self.wait(10) 
        
        self.play(FadeOut(problem_group))

        # --- Slide 2: Countdown ---
        # A simple countdown from 5 to 1
        for i in range(5, 0, -1):
            number = Text(str(i), font_size=96)
            self.play(FadeIn(number, run_time=0.4))
            self.wait(0.2)
            self.play(FadeOut(number, run_time=0.4))

# --- Slide 4: The Pentagon Example ---
        # 1. Setup the Plot Elements
        grid = NumberPlane(
            x_range=[-1, 3, 1],
            y_range=[-1, 3, 1],
            background_line_style={"stroke_color": TEAL, "stroke_opacity": 0.4},
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        )
        grid.add_coordinates(font_size=20)

        # logical coordinates (data)
        coords = [
            [0, 0, 0], [1, 0, 0], [2, 1, 0], [1, 2, 0], [0, 1, 0]
        ]
        
        # FIX: Convert logical coords to grid positions using c2p
        # This ensures (0,0) on the polygon lands on (0,0) of the grid
        grid_points = [grid.c2p(x, y) for x, y, z in coords]

        # Render the polygon using the grid_points
        polygon = Polygon(*grid_points, color=BLUE_E, stroke_width=4, fill_color=BLUE, fill_opacity=0.5)
        
        # Create dots at the calculated grid points
        dots = VGroup(*[Dot(point=p, color=RED, radius=0.1) for p in grid_points])
        
        # Add coordinate labels (positioned relative to the dots, which are now correct)
        labels = VGroup(
            Text("(0,0)", font_size=16).next_to(dots[0], DL, buff=0.1),
            Text("(1,0)", font_size=16).next_to(dots[1], DR, buff=0.1),
            Text("(2,1)", font_size=16).next_to(dots[2], RIGHT, buff=0.1),
            Text("(1,2)", font_size=16).next_to(dots[3], UP, buff=0.1),
            Text("(0,1)", font_size=16).next_to(dots[4], LEFT, buff=0.1),
        )

        # Group all plot elements
        plot_group = VGroup(grid, polygon, dots, labels)

        # 2. Setup the Text Element
        area_text = Text("Area = 5/2", font_size=48)

        # 3. Arrange them side-by-side
        # Now when you arrange them, the polygon is "stuck" to the grid correctly
        layout_group = VGroup(area_text, plot_group).arrange(RIGHT, buff=2)
        
        # 4. Animate Slide 4
        self.play(Create(grid), run_time=1.5)
        self.play(
            DrawBorderThenFill(polygon),
            ShowIncreasingSubsets(dots),
            run_time=2
        )
        self.play(Write(labels))
        self.play(Write(area_text))
        self.wait(3)

        # --- Transition to Slide 5 ---
        # Fade out the text and labels, keep the polygon and grid
        self.play(
            FadeOut(area_text),
            FadeOut(labels),
        )

        # --- Slide 1: Introduction ---
        intro_text = Text("Here we use pick's theorem", font_size=48)
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))



        # --- Slide 5: Applying Pick's Theorem ---
        # The 'plot_group' (without labels) is already on the right side.
        # We will build the text column on the left.

        picks_title = Text("Pick's theorem applied to this example", font_size=28)
        boundary_text = Text("5 boundary points", font_size=24, t2c={"5": RED})
        interior_text = Text("1 interior point", font_size=24, t2c={"1": YELLOW})
        calc_title = Text("Area =", font_size=24)

        # Formula parts for step-by-step animation
        calc_I = Text("1", font_size=24, color=YELLOW)
        calc_plus = Text("+", font_size=24)
        calc_B = Text("5", font_size=24, color=RED)
        calc_div2 = Text("/2", font_size=24)
        calc_minus1 = Text("- 1", font_size=24)
        calc_result = Text("= 5/2", font_size=24)
        
        formula_group = VGroup(calc_I, calc_plus, calc_B, calc_div2, calc_minus1, calc_result).arrange(RIGHT, buff=0.1)

        # Arrange all text elements in a column
        text_column = VGroup(
            picks_title,
            boundary_text,
            interior_text,
            calc_title,
            formula_group
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        
        # Position the text column to the left of the plot
        text_column.next_to(plot_group, LEFT, buff=1)

        # 1. Animate Title
        self.play(Write(picks_title))
        self.wait(0.5)

        # 2. Animate Boundary Points
        self.play(Write(boundary_text))
        # Highlight the vertices (boundary points)
        self.play(
            LaggedStart(*[Indicate(dot, scale_factor=1.5, color=RED_A) for dot in dots], lag_ratio=0.1)
        )
        self.wait(0.5)
        
        # This ensures the dot hits (1,1) on the grid, even if the grid moved
        interior_point = Dot(point=grid.c2p(1, 1), color=YELLOW, radius=0.1)
        self.play(Write(interior_text))
        # Show the interior point
        self.play(GrowFromCenter(interior_point))
        self.play(Indicate(interior_point, scale_factor=1.5))
        self.wait(0.5)

        # 4. Animate Calculation
        self.play(Write(calc_title))

        # Animate numbers flowing from the text to the formula
        # FIX: Use index [0] because the number is the first character in the string
        self.play(TransformFromCopy(interior_text[0], calc_I)) 
        self.play(Write(calc_plus))
        self.play(TransformFromCopy(boundary_text[0], calc_B))
        self.play(Write(calc_div2))
        self.wait(0.5)
        self.play(Write(calc_minus1))
        self.wait(1)
        self.play(Write(calc_result))

        # Final wait
        self.wait(5)

        # --- TRANSITION / CLEANUP ---
        # Fade out all elements to clear the screen for the next section
        self.play(
            FadeOut(plot_group),      # Removes the grid, polygon, and red dots
            FadeOut(text_column),     # Removes the text on the left
            FadeOut(interior_point),  # Removes the yellow interior point
            run_time=1.5
        )
        
        # Optional: explicit wait before the next scene starts
        self.wait(1)

        # --- Setup for visual consistency ---
        # We recreate the grid and polygon state to match where we left off, 
        # or start fresh if running separately.
        
        # 1. Text Style
        def create_text_column(text_lines, scale=0.7):
            grp = VGroup(*[Text(line, font_size=32) for line in text_lines])
            grp.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            return grp
        
        
                # --- Slide 11: Area Formula Proof ---
        title_area = Text("Since we have 5 points on the border", font_size=40)
        title_area.to_edge(UP, buff=1)

        math_block = VGroup(
            Text("The area of the pentagon is", font_size=32),
            MathTex(r"\text{Area} = I + \frac{B}{2} - 1", font_size=48),
            MathTex(r"\text{Area} = I + \frac{5}{2} - 1", font_size=48),
            MathTex(r"\text{Area} = I + \frac{3}{2}", font_size=48, color=YELLOW),
            Text("So we need to show #interior points >= 1", font_size=36, color=RED)
        ).arrange(DOWN, buff=0.6)

        self.play(Write(title_area))
        self.play(Write(math_block[0]))
        self.play(Write(math_block[1]))
        self.wait(1)
        self.play(TransformMatchingTex(math_block[1].copy(), math_block[2]))
        self.wait(1)
        self.play(TransformMatchingTex(math_block[2], math_block[3]))
        self.play(Write(math_block[4]))
        self.wait(6)

        self.play(FadeOut(title_area), FadeOut(math_block))

        # --- Slide 6: Pigeonhole Principle ---
        title_php = Text("Pigeonhole principle!", font_size=48, color=YELLOW)

        text_php = VGroup(
            Text("Since each coordinate can be either even or odd, there", font_size=32),
            Text("Are 4 configurations: (E,E), (O,O), (O,E), (E,O)", font_size=32, t2c={"(E,E)": BLUE, "(O,O)": BLUE, "(O,E)": BLUE, "(E,O)": BLUE}),
            Text("That means at least two points must have the same configuration!", font_size=32, color=RED)
        ).arrange(DOWN, buff=0.8)

        self.play(Write(title_php))
        self.play(
            FadeOut(title_php),      # Removes the PHP text
            run_time=1.5
        )

        self.play(FadeIn(text_php, shift=UP))
        self.wait(6) # Time to think
        
        self.play(FadeOut(text_php))


        # --- Slide 7: Visualizing the Pairs ---
        # Setup Plot
        grid = NumberPlane(
            x_range=[-1, 3, 1],
            y_range=[-1, 3, 1],
            background_line_style={"stroke_color": TEAL, "stroke_opacity": 0.4},
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).add_coordinates()

        # 1. Define Logical Coordinates (Data)
        # We keep the data separate from the screen positions
        coords = [[0, 0, 0], [1, 0, 0], [2, 1, 0], [1, 2, 0], [0, 1, 0]]
        
        # 2. Convert to Screen Positions using grid.c2p
        # This ensures the points land exactly on the grid lines
        screen_points = [grid.c2p(x, y) for x, y, z in coords]

        # 3. Create Geometry using Screen Positions
        polygon = Polygon(*screen_points, color=BLUE_E, stroke_width=4, fill_color=BLUE, fill_opacity=0.5)
        dots = VGroup(*[Dot(point=p, color=RED, radius=0.08) for p in screen_points])
        
        # Labels for vertices (positioned relative to the dots)
        labels = VGroup(
            Text("(0,0)", font_size=16).next_to(dots[0], DL, buff=0.1),
            Text("(1,0)", font_size=16).next_to(dots[1], DR, buff=0.1),
            Text("(2,1)", font_size=16).next_to(dots[2], RIGHT, buff=0.1),
            Text("(1,2)", font_size=16).next_to(dots[3], UP, buff=0.1),
            Text("(0,1)", font_size=16).next_to(dots[4], LEFT, buff=0.1),
        )
        
        plot_group = VGroup(grid, polygon, dots, labels)
        plot_group.to_edge(RIGHT, buff=0.5)

        # Text for Slide 7
        slide7_text = VGroup(
            Text("In this example, there", font_size=32),
            Text("Are two such pairs:", font_size=32),
            Text("Colored in green and", font_size=32),
            Text("pink", font_size=32, color=PINK)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_edge(LEFT, buff=1)
        
        # Boxes for specific vertices
        # Note: We attach these to the 'dots' which are already correctly positioned
        # Pair 1: (1,2) and (1,0) -> dots[3] and dots[1]
        box_top = SurroundingRectangle(dots[3], color=GREEN, buff=0.15)
        box_bot_mid = SurroundingRectangle(dots[1], color=GREEN, buff=0.15)
        
        # Pair 2: (0,1) and (2,1) -> dots[4] and dots[2]
        box_left = SurroundingRectangle(dots[4], color=PINK, buff=0.15)
        box_right = SurroundingRectangle(dots[2], color=PINK, buff=0.15)

        self.play(Create(grid), DrawBorderThenFill(polygon), Create(dots), Write(labels))
        self.play(Write(slide7_text))
        self.wait(2)
        
        self.play(Create(box_top), Create(box_bot_mid))
        self.play(Create(box_left), Create(box_right))
        self.wait(5) 

        # --- Slide 8: Midpoint Logic (Diagonally Connected) ---
        self.play(FadeOut(slide7_text))
        
        slide8_text = VGroup(
            Text("For any pair with", font_size=32),
            Text("same parity,", font_size=32),
            Text("Find their midpoint!", font_size=32, color=YELLOW),
            Text("If the pair is diagonally", font_size=32),
            Text("connected,", font_size=32),
            Text("Their midpoint will be", font_size=32),
            Text("an interior point!", font_size=32, color=RED)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_edge(LEFT, buff=0.5)

        self.play(Write(slide8_text[:3]))
        
        # Animate the midpoint for Green Pair (1,2) and (1,0)
        # FIX: Use grid.c2p for the midpoint (1,1) so it lands on the intersection
        # FIX: Draw the line between the actual dot objects to ensure connection
        midpoint_line = Line(dots[3].get_center(), dots[1].get_center(), color=GREEN)
        
        midpoint_coords = grid.c2p(1, 1)
        midpoint_dot = Dot(point=midpoint_coords, color=RED, radius=0.15)
        
        midpoint_label = Text("(1,1)", font_size=24, color=RED).next_to(midpoint_dot, RIGHT)

        self.play(Create(midpoint_line))
        self.play(ScaleInPlace(midpoint_dot, 1.2), Write(midpoint_label))
        
        self.play(Write(slide8_text[3:]))
        self.play(Indicate(midpoint_dot, scale_factor=1.5))
        self.wait(6)

# --- Slide 9: Boundary Case (Adjacent) ---
        # 1. Cleanup everything from previous slides
        # We remove slide8_text and all its specific visuals.
        # Crucially, we also remove the entire plot_group from Slide 7/8.
        self.play(
            FadeOut(slide8_text),
            FadeOut(midpoint_line),
            FadeOut(midpoint_dot),
            FadeOut(midpoint_label),
            FadeOut(box_left), FadeOut(box_right),
            FadeOut(box_top), FadeOut(box_bot_mid),
            FadeOut(plot_group) # <-- Removes the old polygon and grid completely
        )

        # 2. Setup Text for Slide 9
        slide9_text = VGroup(
            Text("But the pairs", font_size=32),
            Text("with same", font_size=32),
            Text("parity could", font_size=32),
            Text("also be", font_size=32),
            Text("adjacent.", font_size=32),
            Text("Then the", font_size=32),
            Text("midpoint", font_size=32),
            Text("Will be on the", font_size=32),
            Text("boundary and we", font_size=32),
            Text("have reduced it", font_size=32),
            Text("to a subproblem.", font_size=32),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(LEFT, buff=0.5)

        # 3. Setup New Plot with NEW coordinates
        new_grid = NumberPlane(
            x_range=[-1, 4, 1], # Slightly wider range to fit x=3
            y_range=[-1, 3, 1],
            background_line_style={"stroke_color": TEAL, "stroke_opacity": 0.4},
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).add_coordinates()

        # The new set of vertices as requested
        new_coords = [[0, 0, 0], [2, 0, 0], [3, 1, 0], [1, 2, 0], [0, 1, 0]]
        # Convert to screen positions so they lock to the grid
        new_screen_points = [new_grid.c2p(x, y) for x, y, z in new_coords]

        # Create the polygon and dots with same style as before
        new_polygon = Polygon(*new_screen_points, color=BLUE_E, stroke_width=4, fill_color=BLUE, fill_opacity=0.5)
        new_dots = VGroup(*[Dot(point=p, color=RED, radius=0.08) for p in new_screen_points])

        # Let's add labels for the relevant points (0,0) and (2,0) for clarity
        new_labels = VGroup(
            Text("(0,0)", font_size=16).next_to(new_dots[0], DL, buff=0.1),
            Text("(2,0)", font_size=16).next_to(new_dots[1], DR, buff=0.1),
        )
        
        # Group and position the new plot
        new_plot_group = VGroup(new_grid, new_polygon, new_dots, new_labels)
        new_plot_group.to_edge(RIGHT, buff=0.5)

        # 4. Animate Text and New Plot creation
        self.play(Write(slide9_text))
        # Draw the new scene from scratch
        self.play(Create(new_grid), DrawBorderThenFill(new_polygon), Create(new_dots), Write(new_labels))
        self.wait(1)

        # 5. Visualize the "Adjacent Parity" case
        # The vertices are (0,0) and (2,0). Both are (Even, Even).
        # They are adjacent in our list: new_dots[0] and new_dots[1].
        
        # Highlight them with boxes (Green for "same parity", consistent with previous slide)
        box_origin = SurroundingRectangle(new_dots[0], color=GREEN, buff=0.15)
        box_two_zero = SurroundingRectangle(new_dots[1], color=GREEN, buff=0.15)
        
        # Connect them with a line to show it's a boundary segment
        # We use the positions of the dots to ensure the line is placed correctly
        boundary_line = Line(new_dots[0].get_center(), new_dots[1].get_center(), color=GREEN, stroke_width=4)
        
        # Show the midpoint (1,0)
        # Calculate screen position for (1,0)
        midpoint_coord_bound = new_grid.c2p(1, 0)
        mid_boundary_dot = Dot(midpoint_coord_bound, color=RED, radius=0.15)
        mid_label_bound = Text("(1,0)", font_size=24, color=RED).next_to(mid_boundary_dot, UP)
        
        # Execute animation sequence for the logic
        self.play(Create(box_origin), Create(box_two_zero))
        self.wait(0.5)
        self.play(Create(boundary_line))
        # Pop the midpoint dot and label into existence
        self.play(ScaleInPlace(mid_boundary_dot, 1.2), Write(mid_label_bound))
        # Emphasize the midpoint lying on the boundary
        self.play(Indicate(mid_boundary_dot, scale_factor=1.5))
        self.wait(6)

# --- Slide 10: Reduction Step (Green Polygon) ---
        
        # 1. Cleanup Slide 9
        # We must fade out the elements created in the previous step.
        # Note: 'new_plot_group' contains the grid, blue polygon, and red dots from Slide 9.
        self.play(
            FadeOut(new_plot_group), 
            FadeOut(slide9_text),
            FadeOut(boundary_line),
            FadeOut(mid_boundary_dot),
            FadeOut(mid_label_bound),
            FadeOut(box_origin),
            FadeOut(box_two_zero)
        )

        # 2. Setup Text
        slide10_text = VGroup(
            Text("Here we can repeat", font_size=36),
            Text("the process: find the", font_size=36),
            Text("pair with same parity.", font_size=36),
            Text("If they are across, we", font_size=36),
            Text("are done.", font_size=36),
            Text("Otherwise, we", font_size=36),
            Text("reduce.", font_size=36),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_edge(LEFT)

        # 3. Setup Green Reduction Polygon
        grid_reduce = NumberPlane(
            x_range=[-1, 4, 1],
            y_range=[-1, 3, 1],
            background_line_style={"stroke_color": TEAL, "stroke_opacity": 0.4},
            axis_config={"stroke_color": WHITE, "stroke_width": 2}
        ).add_coordinates()
        
        # New vertices for the reduction case
        reduce_coords = [[0,0,0], [1,0,0], [3,1,0], [1,2,0], [0,1,0]]
        
        # Convert to screen coordinates
        reduce_screen_points = [grid_reduce.c2p(x, y) for x, y, z in reduce_coords]

        # Create geometry
        reduce_polygon = Polygon(*reduce_screen_points, color=GREEN, fill_color=GREEN, fill_opacity=0.3)
        reduce_dots = VGroup(*[Dot(point=p, color=RED, radius=0.08) for p in reduce_screen_points])
        
        # Create Labels
        reduce_labels = VGroup(
            Text("(0,0)", font_size=16, color=RED).next_to(reduce_dots[0], DL, buff=0.1),
            Text("(1,0)", font_size=16, color=RED).next_to(reduce_dots[1], DR, buff=0.1),
            Text("(3,1)", font_size=16, color=RED).next_to(reduce_dots[2], RIGHT, buff=0.1),
            Text("(1,2)", font_size=16, color=RED).next_to(reduce_dots[3], UP, buff=0.1),
            Text("(0,1)", font_size=16, color=RED).next_to(reduce_dots[4], LEFT, buff=0.1),
        )

        reduce_group = VGroup(grid_reduce, reduce_polygon, reduce_dots, reduce_labels)
        reduce_group.to_edge(RIGHT, buff=0.5)

        # 4. Animate
        self.play(Write(slide10_text))
        self.play(
            Create(grid_reduce), 
            DrawBorderThenFill(reduce_polygon), 
            Create(reduce_dots), 
            Write(reduce_labels)
        )
        self.wait(6)
        # --- Transition / Cleanup after Slide 10 ---
        self.play(
            FadeOut(reduce_group),
            FadeOut(slide10_text)
        )
        self.wait(1)

        # --- Slide 12: Conclusion ---
        final_text = VGroup(
            Text("Our reduction will end in finite steps, so we", font_size=40),
            Text("Can always find an interior point!", font_size=40),
            Text("And we are done.", font_size=40)
        ).arrange(DOWN, buff=1)

        self.play(Write(final_text[0]))
        self.wait(2)
        self.play(Write(final_text[1]))
        self.wait(2)
        self.play(Write(final_text[2]))
        
        self.wait(5)