from manim import *

class BalancedStringsSolution(Scene):
    def construct(self):
        self.intro_problem()
        self.random_walk_transformation()
        self.visualize_constraint()
        self.analyze_cases()
        self.inclusion_exclusion()

    def intro_problem(self):
        """
        Introduction to the problem statement and definition of Balanced Strings.
        """
        title = Tex("Putnam 1996 B5: Balanced Binary Strings").scale(0.9).to_edge(UP)
        self.play(Write(title))
        
        # Definition of Delta
        delta_def = MathTex(r"\Delta(S) = n(X) - n(O)").move_to(UP * 2)
        self.play(Write(delta_def))
        self.wait(1)

        # Example String
        ex_text = Text("Example:", font_size=24).next_to(delta_def, DOWN, buff=0.5).to_edge(LEFT, buff=2)
        string_str = "XOOXOOX"
        s_mob = MathTex(*list(string_str)).next_to(delta_def, DOWN, buff=0.5)
        
        self.play(Write(ex_text), Write(s_mob))
        
        # Calculate Delta for the whole string
        # X=3, O=4, Delta = -1
        calc_text = MathTex(r"\Delta(\text{XOOXOOX}) = 3 - 4 = -1").next_to(s_mob, DOWN)
        self.play(Write(calc_text))
        self.wait(2)

        # Define Balanced
        balanced_def_text = Text("A string is Balanced if for EVERY substring T:", font_size=32).next_to(calc_text, DOWN, buff=1)
        balanced_cond = MathTex(r"-2 \leq \Delta(T) \leq 2").next_to(balanced_def_text, DOWN)
        
        self.play(FadeIn(balanced_def_text))
        self.play(Write(balanced_cond))
        self.play(Indicate(balanced_cond, color=YELLOW))
        self.wait(3)

        # Show an example of checking substrings
        # We will simulate checking a few substrings
        brace = Brace(s_mob[1:4], DOWN, buff=0.1) # OOX
        sub_calc = MathTex(r"\Delta(\text{OOX}) = 1 - 2 = -1").next_to(brace, DOWN)
        check_mark = MathTex(r"\checkmark", color=GREEN).next_to(sub_calc, RIGHT)

        self.play(GrowFromCenter(brace), Write(sub_calc))
        self.wait(1)
        self.play(Write(check_mark))
        self.wait(1)
        
        # Show an IMBALANCED example
        self.play(
            FadeOut(s_mob), FadeOut(calc_text), FadeOut(brace), 
            FadeOut(sub_calc), FadeOut(check_mark), FadeOut(balanced_def_text), FadeOut(balanced_cond)
        )

        bad_string_str = "X X X O"
        bad_mob = MathTex(*list("XXXO")).move_to(s_mob.get_center())
        bad_label = Text("Imbalanced Example:", font_size=24).next_to(bad_mob, LEFT, buff=0.5)
        
        self.play(Write(bad_mob), Write(bad_label))
        self.wait(1)

        # Highlight the bad substring
        brace_bad = Brace(bad_mob[0:3], DOWN, buff=0.1) # XXX
        bad_calc = MathTex(r"\Delta(\text{XXX}) = 3 - 0 = 3").next_to(brace_bad, DOWN)
        cross_mark = MathTex(r"\times", color=RED).next_to(bad_calc, RIGHT)
        
        self.play(GrowFromCenter(brace_bad))
        self.play(Write(bad_calc))
        self.play(Write(cross_mark))
        
        warning = Text("Violates condition!", color=RED, font_size=24).next_to(cross_mark, RIGHT)
        self.play(Write(warning))
        self.wait(3) # Time to absorb

        self.clear()
        self.title = title # Keep title
        self.add(title)

    def random_walk_transformation(self):
        """
        Translate the string problem into a geometric random walk.
        """
        header = Text("Geometric Interpretation: Random Walk", font_size=36).to_edge(UP, buff=1.5)
        self.play(Write(header))

        # Setup Axis
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-3, 4, 1],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True}
        ).move_to(DOWN * 0.5)
        
        labels = axes.get_axis_labels(x_label="k (index)", y_label="S_k (Sum)")
        self.play(Create(axes), Write(labels))

        # Rules
        rule_x = MathTex(r"X \rightarrow +1 \text{ (Up)}").to_edge(LEFT).shift(UP*2)
        rule_o = MathTex(r"O \rightarrow -1 \text{ (Down)}").next_to(rule_x, DOWN)
        start_rule = MathTex(r"S_0 = 0").next_to(rule_o, DOWN)
        
        self.play(Write(rule_x), Write(rule_o), Write(start_rule))
        self.wait(2)

        # Animate a path for X O X X O
        # Path: (0,0) -> (1,1) -> (2,0) -> (3,1) -> (4,2) -> (5,1)
        points = [
            axes.coords_to_point(0, 0),
            axes.coords_to_point(1, 1),
            axes.coords_to_point(2, 0),
            axes.coords_to_point(3, 1),
            axes.coords_to_point(4, 2),
            axes.coords_to_point(5, 1),
        ]
        
        path = VMobject(color=BLUE, stroke_width=4)
        path.set_points_as_corners(points)
        
        dots = VGroup(*[Dot(p, color=YELLOW) for p in points])
        
        self.play(Create(dots[0]))
        for i in range(len(points)-1):
            self.play(Create(Line(points[i], points[i+1], color=BLUE)), Create(dots[i+1]), run_time=0.5)
        
        self.wait(2)

        # Explain Substrings
        expl_text = Text("Substring from i to j = Path from step i to j", font_size=28).to_edge(RIGHT).shift(UP)
        self.play(Write(expl_text))
        
        # Highlight a segment (e.g., index 2 to 4)
        # S_2 = 0, S_4 = 2. Diff = 2.
        p1 = dots[2]
        p2 = dots[4]
        
        brace_diff = Brace(VGroup(p1, p2), RIGHT)
        diff_text = MathTex(r"\Delta(T) = S_j - S_i").next_to(brace_diff, RIGHT)
        
        self.play(Indicate(p1), Indicate(p2))
        self.play(Create(brace_diff), Write(diff_text))
        self.wait(3)
        
        self.play(FadeOut(path), FadeOut(dots), FadeOut(brace_diff), FadeOut(diff_text), FadeOut(expl_text))
        self.axes = axes # Save for next method

    def visualize_constraint(self):
        """
        Explain why |Si - Sj| <= 2 implies the whole path must fit in range of size 2.
        """
        axes = self.axes
        
        constraint_text = MathTex(r"|\Delta(T)| \le 2 \iff |S_j - S_i| \le 2").to_edge(UP, buff=2)
        self.play(Write(constraint_text))
        self.wait(2)

        # "What if the path spans 3 units?"
        question = Text("What if the span is 3?", color=RED, font_size=32).next_to(constraint_text, DOWN)
        self.play(Write(question))

        # Draw a path that goes from 0 to 3
        # (0,0) -> (1,1) -> (2,2) -> (3,3)
        bad_points = [
            axes.coords_to_point(0, 0),
            axes.coords_to_point(1, 1),
            axes.coords_to_point(2, 2),
            axes.coords_to_point(3, 3),
        ]
        bad_path = VMobject(color=RED, stroke_width=4).set_points_as_corners(bad_points)
        self.play(Create(bad_path))
        
        # Show the difference between start and end
        line_bottom = DashedLine(axes.coords_to_point(0,0), axes.coords_to_point(3,0), color=GRAY)
        line_top = DashedLine(axes.coords_to_point(0,3), axes.coords_to_point(3,3), color=GRAY)
        dist_arrow = DoubleArrow(axes.coords_to_point(3,0), axes.coords_to_point(3,3), buff=0, color=RED)
        dist_label = MathTex("3").next_to(dist_arrow, RIGHT)

        self.play(Create(line_bottom), Create(line_top))
        self.play(Create(dist_arrow), Write(dist_label))
        self.wait(1)
        
        conclusion = Text("This substring implies \n" + r"$\Delta = 3 > 2$. Impossible!", font_size=28, color=RED).next_to(dist_label, RIGHT)
        self.play(Write(conclusion))
        self.wait(4) # Allow user to process logic

        # Conclusion text
        final_logic = Text("The path is confined to a vertical strip of height 2.", font_size=32, color=GREEN).move_to(UP*0.5)
        self.play(FadeOut(bad_path), FadeOut(line_bottom), FadeOut(line_top), FadeOut(dist_arrow), FadeOut(dist_label), FadeOut(question), FadeOut(conclusion))
        self.play(Write(final_logic))
        self.wait(3)
        
        self.clear() 

    def analyze_cases(self):
        """
        Show the three valid sets of integers.
        """
        title = Text("Since we start at 0, there are only 3 valid 'Universes'", font_size=32).to_edge(UP)
        self.play(Write(title))

        # Draw Number Line
        number_line = NumberLine(
            x_range=[-3, 3, 1],
            length=8,
            include_numbers=True
        ).shift(DOWN)
        self.play(Create(number_line))
        
        start_dot = Dot(number_line.n2p(0), color=YELLOW, radius=0.15)
        self.play(Create(start_dot))
        
        # Case A: {-1, 0, 1}
        rect_a = Rectangle(width=number_line.n2p(1)[0] - number_line.n2p(-1)[0] + 0.5, height=1, color=BLUE)
        rect_a.move_to(number_line.n2p(0))
        label_a = MathTex(r"A: \{-1, 0, 1\}").next_to(rect_a, UP)
        
        self.play(Create(rect_a), Write(label_a))
        self.wait(1)
        
        # Explanation of logic for A
        # Start at 0. Can go to -1 or 1.
        # If at 1, MUST go to 0 (can't go to 2).
        logic_text = Text("From 1 or -1, must return to 0.", font_size=24, color=BLUE).to_edge(UP, buff=2)
        self.play(Write(logic_text))
        
        # Show small bouncing dots
        dot_anim = Dot(color=BLUE)
        dot_anim.move_to(number_line.n2p(0))
        self.add(dot_anim)
        self.play(dot_anim.animate.move_to(number_line.n2p(1)), run_time=0.5)
        self.play(dot_anim.animate.move_to(number_line.n2p(0)), run_time=0.5)
        self.play(dot_anim.animate.move_to(number_line.n2p(-1)), run_time=0.5)
        self.play(dot_anim.animate.move_to(number_line.n2p(0)), run_time=0.5)
        self.remove(dot_anim)
        
        count_a = MathTex(r"|A| = 2^{\lceil n/2 \rceil}").next_to(rect_a, DOWN)
        self.play(Write(count_a))
        self.wait(3)
        
        self.play(FadeOut(rect_a), FadeOut(label_a), FadeOut(count_a), FadeOut(logic_text))

        # Case B: {0, 1, 2}
        rect_b = Rectangle(width=number_line.n2p(2)[0] - number_line.n2p(0)[0] + 0.5, height=1, color=GREEN)
        # Center at 1
        rect_b.move_to(number_line.n2p(1))
        label_b = MathTex(r"B: \{0, 1, 2\}").next_to(rect_b, UP)
        
        self.play(Create(rect_b), Write(label_b))
        
        logic_text_b = Text("Start 0 -> 1 (forced). Then bounce.", font_size=24, color=GREEN).to_edge(UP, buff=2)
        self.play(Write(logic_text_b))
        
        count_b = MathTex(r"|B| = 2^{\lfloor n/2 \rfloor}").next_to(rect_b, DOWN)
        self.play(Write(count_b))
        self.wait(3)
        
        self.play(FadeOut(rect_b), FadeOut(label_b), FadeOut(count_b), FadeOut(logic_text_b))

        # Case C: {-2, -1, 0}
        rect_c = Rectangle(width=number_line.n2p(0)[0] - number_line.n2p(-2)[0] + 0.5, height=1, color=ORANGE)
        rect_c.move_to(number_line.n2p(-1))
        label_c = MathTex(r"C: \{-2, -1, 0\}").next_to(rect_c, UP)
        
        self.play(Create(rect_c), Write(label_c))
        count_c = MathTex(r"|C| = 2^{\lfloor n/2 \rfloor}").next_to(rect_c, DOWN)
        self.play(Write(count_c))
        self.wait(3)
        
        self.clear()

    def inclusion_exclusion(self):
        """
        Final calculation using I-E Principle.
        """
        title = Text("Total Count: Inclusion-Exclusion", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Formula
        formula = MathTex(r"|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C|")
        formula.scale(0.8).shift(UP)
        self.play(Write(formula))
        self.wait(2)

        # Substitutions
        term_a = MathTex(r"|A| = 2^{\lceil n/2 \rceil}", color=BLUE).shift(LEFT * 4)
        term_bc = MathTex(r"|B| = |C| = 2^{\lfloor n/2 \rfloor}", color=GREEN).next_to(term_a, DOWN, aligned_edge=LEFT)
        
        self.play(Write(term_a), Write(term_bc))
        self.wait(2)

        # Intersections
        inter_title = Text("Intersections:", font_size=28).shift(RIGHT * 2 + UP * 0.5)
        self.play(Write(inter_title))

        # A intersect B = {0, 1}
        ab_text = MathTex(r"A \cap B = \{0, 1\} \rightarrow 1 \text{ path}", font_size=32).next_to(inter_title, DOWN)
        ac_text = MathTex(r"A \cap C = \{0, -1\} \rightarrow 1 \text{ path}", font_size=32).next_to(ab_text, DOWN)
        bc_text = MathTex(r"B \cap C = \{0\} \rightarrow 0 \text{ paths}", font_size=32).next_to(ac_text, DOWN)

        self.play(Write(ab_text))
        self.wait(1)
        self.play(Write(ac_text))
        self.wait(1)
        self.play(Write(bc_text))
        self.wait(2)

        # Final Sum
        final_line = MathTex(r"Total = 2^{\lceil n/2 \rceil} + 2 \cdot 2^{\lfloor n/2 \rfloor} - 2").shift(DOWN * 2.5)
        box = SurroundingRectangle(final_line, color=YELLOW)
        
        self.play(Write(final_line))
        self.play(Create(box))
        self.wait(3)

        # N even vs N odd
        even_case = MathTex(r"\text{Even } n: \quad 3 \cdot 2^{n/2} - 2").scale(0.8).to_corner(DL)
        odd_case = MathTex(r"\text{Odd } n: \quad 2^{(n+3)/2} - 2").scale(0.8).to_corner(DR)

        self.play(Write(even_case), Write(odd_case))
        self.wait(5)