from manim import *
import numpy as np

class p2(Scene):
    def construct(self):
        # constants
        config_math = {
            "f": lambda t, x: x - t**2 + 1,
            "exact_sol": lambda t: (t + 1)**2 - 0.5 * np.exp(t),
            "t0": 0,
            "x0": 0.5,
            "h": 0.5,
            "steps": 4,
            "t_range": [0, 2],
            "latex_sol": r"x(t) = (t+1)^2 - 0.5e^t"
        }

        self.camera.frame_width = 28
        self.camera.frame_height = 16

        axes = Axes(
            x_range=[0, 2.2, 0.5],
            y_range=[0, 6.5, 1],
            x_length=20,
            y_length=12,
            axis_config={"include_numbers": True, "font_size": 40, "stroke_width": 4},
        ).shift(DOWN * 0.5)

        # labels = axes.get_axis_labels(
        #     x_label=MathTex("t", font_size=60), 
        #     y_label=MathTex("x", font_size=60)
        # )
        
        self.play(Create(axes))

        exact_graph = axes.plot(
            config_math["exact_sol"], 
            color=BLUE, 
            x_range=config_math["t_range"], 
            stroke_width=6
        )
        exact_label = MathTex(config_math["latex_sol"], color=BLUE, font_size=48)
        exact_label.next_to(axes.c2p(1.2, 5.5), UR)

        self.play(Create(exact_graph), Write(exact_label))

        t, x = config_math["t0"], config_math["x0"]
        h = config_math["h"]
        
        current_dot = Dot(axes.c2p(t, x), color=YELLOW, radius=0.15)
        self.add(current_dot)

        euler_points = [(t, x)]

        for i in range(config_math["steps"]):
            slope = config_math["f"](t, x)
            t_next, x_next = t + h, x + h * slope

            line = Line(axes.c2p(t, x), axes.c2p(t_next, x_next), color=RED, stroke_width=5)
            next_dot = Dot(axes.c2p(t_next, x_next), color=YELLOW, radius=0.15)
            coord_label = MathTex(f"({t_next:.1f}, {x_next:.2f})", font_size=34)\
                          .next_to(next_dot, DR, buff=0.1)

            self.play(
                Create(line),
                FadeIn(next_dot),
                Write(coord_label),
                run_time=0.8
            )

            t, x = t_next, x_next
            euler_points.append((t, x))

        t_final, x_final_euler = euler_points[-1]
        x_final_exact = config_math["exact_sol"](t_final)

        p_euler = axes.c2p(t_final, x_final_euler)
        p_exact = axes.c2p(t_final, x_final_exact)

        error_brace = BraceBetweenPoints(p_euler, p_exact, direction=RIGHT, color=GREEN)
        error_text = error_brace.get_text("Global Error").set_color(GREEN)

        self.play(Create(error_brace), Write(error_text))
        self.wait(3)


class p3(Scene):
    def construct(self):
        self.camera.frame_width = 17.5
        self.camera.frame_height = 10
        # constants
        L = 1.0
        g = 9.8
        initial_theta = PI / 4
        initial_w = 0.0
        t_max = 10
        sim_dt = 0.01

        def pendulum_ode(t, y):
            theta, w = y
            return [w, -(g / L) * np.sin(theta)]

        def rk4_step(f, t, y, dt):
            k1 = np.array(f(t, y))
            k2 = np.array(f(t + dt/2, y + dt/2 * k1))
            k3 = np.array(f(t + dt/2, y + dt/2 * k2))
            k4 = np.array(f(t + dt, y + dt * k3))
            return y + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)

        time_points = np.arange(0, t_max + sim_dt, sim_dt)
        state_history = np.zeros((len(time_points), 2))
        state_history[0] = [initial_theta, initial_w]

        current_y = state_history[0]
        for i in range(1, len(time_points)):
            current_y = rk4_step(pendulum_ode, time_points[i-1], current_y, sim_dt)
            state_history[i] = current_y

        t_data = time_points
        theta_data = state_history[:, 0]
        w_data = state_history[:, 1]

        pivot = LEFT * 4.0 + UP * 1.5
        rod_length = 2.5 
        
        pivot_dot = Dot(color=RED).move_to(pivot)
        bob = Dot(radius=0.15, color=BLUE_E)
        rod = Line(start=pivot, end=bob.get_center(), stroke_width=4, color=BLUE_E)
        pendulum = VGroup(rod, bob)

        def get_pendulum_pos(theta):
            return pivot + DOWN * rod_length * np.cos(theta) + RIGHT * rod_length * np.sin(theta)

        bob.move_to(get_pendulum_pos(initial_theta))
        rod.put_start_and_end_on(pivot, bob.get_center())

        top_right_area = VGroup()

        traj_axes = Axes(
            x_range=[0, 10.5, 2],
            y_range=[-0.9, 0.9, 0.2],
            x_length=5.5, # Reduced from 6.5
            y_length=2.5, # Reduced from 3.5
            axis_config={"include_tip": False}
        )
        # traj_labels = traj_axes.get_axis_labels(
        #     x_label=Tex("$t$").scale(0.7), 
        #     y_label=Tex(r"$\theta$").scale(0.7)
        # )
        traj_title = Tex("Trajectory").scale(0.8).move_to(traj_axes.get_top() + UP * 0.3)
        
        full_traj_points = [traj_axes.c2p(t, th) for t, th in zip(t_data, theta_data)]
        full_traj_line = VMobject().set_points_as_corners(full_traj_points).set_stroke(width=1.5, color=BLUE_B)

        top_right_area.add(traj_axes, traj_title, full_traj_line)
        top_right_area.move_to(RIGHT * 3.5 + UP * 1.8) # Adjusted vertical position

        traj_dot = Dot(color=RED, radius=0.07).move_to(full_traj_points[0])

        bottom_right_area = VGroup()

        phase_axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2.6, 2.6, 1.0], 
            x_length=5.5, # Reduced from 6.5
            y_length=2.5, # Reduced from 3.5
            axis_config={"include_tip": False}
        )
        # phase_labels = phase_axes.get_axis_labels(
        #     x_label=Tex(r"$\theta$").scale(0.7), 
        #     y_label=Tex("oh ma ga").scale(0.7)
        # )
        phase_title = Tex("Phase space").scale(0.8).move_to(phase_axes.get_top() + UP * 0.3)

        full_phase_points = [phase_axes.c2p(th, w) for th, w in zip(theta_data, w_data)]
        full_phase_line = VMobject().set_points_as_corners(full_phase_points).set_stroke(width=1.5, color=BLUE_B)

        bottom_right_area.add(phase_axes, phase_title, full_phase_line)
        bottom_right_area.move_to(RIGHT * 3.5 + DOWN * 1.8)

        phase_dot = Dot(color=RED, radius=0.07).move_to(full_phase_points[0])


        self.add(pivot_dot, pendulum)
        self.add(top_right_area, bottom_right_area)
        self.add(traj_dot, phase_dot)

        time_tracker = ValueTracker(0.0)

        def update_pendulum(m, dt):
            t = time_tracker.get_value()
            current_theta = np.interp(t, t_data, theta_data)
            new_bob_pos = get_pendulum_pos(current_theta)
            m[0].put_start_and_end_on(pivot, new_bob_pos) 
            m[1].move_to(new_bob_pos) 
        
        pendulum.add_updater(update_pendulum)

        def update_traj_dot(m, dt):
            t = time_tracker.get_value()
            current_theta = np.interp(t, t_data, theta_data)
            current_point = traj_axes.c2p(t, current_theta)
            m.move_to(current_point)
        
        traj_dot.add_updater(update_traj_dot)

        def update_phase_dot(m, dt):
            t = time_tracker.get_value()
            current_theta = np.interp(t, t_data, theta_data)
            current_w = np.interp(t, t_data, w_data)
            current_point = phase_axes.c2p(current_theta, current_w)
            m.move_to(current_point)
        
        phase_dot.add_updater(update_phase_dot)

        anim_time = 10 
        self.play(time_tracker.animate.set_value(t_max), run_time=anim_time, rate_func=linear)


class p4(Scene):
    def construct(self):
        self.camera.frame_width = 17.5
        self.camera.frame_height = 10

        # constants
        G, L1, L2, M1, M2 = 9.8, 1.0, 1.0, 1.0, 1.0
        dt = 0.01
        t_stop = 10 # dur
        history_len = 500 # lowk useless
        
        th1 = 120.0
        w1 = 0.0
        th2 = -10.0
        w2 = 0.0

        def derivs(t, state):
            dydx = np.zeros_like(state)

            dydx[0] = state[1]

            delta = state[2] - state[0]
            den1 = (M1+M2) * L1 - M2 * L1 * np.cos(delta) * np.cos(delta)
            dydx[1] = ((M2 * L1 * state[1] * state[1] * np.sin(delta) * np.cos(delta)
                        + M2 * G * np.sin(state[2]) * np.cos(delta)
                        + M2 * L2 * state[3] * state[3] * np.sin(delta)
                        - (M1+M2) * G * np.sin(state[0]))
                    / den1)

            dydx[2] = state[3]

            den2 = (L2/L1) * den1
            dydx[3] = ((- M2 * L2 * state[3] * state[3] * np.sin(delta) * np.cos(delta)
                        + (M1+M2) * G * np.sin(state[0]) * np.cos(delta)
                        - (M1+M2) * L1 * state[1] * state[1] * np.sin(delta)
                        - (M1+M2) * G * np.sin(state[2]))
                    / den2)

            return dydx
        
        dt = 0.01
        t = np.arange(0, t_stop, dt)
        
        self.current_state = np.radians([th1, w1, th2, w2])

        y = np.empty((len(t), 4))
        y[0] = self.current_state
        for i in range(1, len(t)):
            y[i] = y[i - 1] + derivs(t[i - 1], y[i - 1]) * dt

        # more accurate estimate could be obtained e.g. using scipy:
        # y = scipy.integrate.solve_ivp(derivs, t[[0, -1]], state, t_eval=t).y.T

        x1 = L1*np.sin(y[:, 0])
        y1 = -L1*np.cos(y[:, 0])

        x2 = L2*np.sin(y[:, 2]) + x1
        y2 = -L2*np.cos(y[:, 2]) + y1

        scale = 2
        origin_point = UP * 1.5 # pendulum has room to swing
        
        # visual objects (positions at index 0)
        dot = Dot(origin_point, radius=0.08, color=WHITE)
        rod1 = Line(origin_point, origin_point + [x1[0]*scale, y1[0]*scale, 0], color=WHITE)
        rod2 = Line(rod1.get_end(), origin_point + [x2[0]*scale, y2[0]*scale, 0], color=WHITE)
        dot1 = Dot(rod1.get_end(), radius=0.10, color=BLUE)
        dot2 = Dot(rod2.get_end(), radius=0.12, color=BLUE)

        trace = TracedPath(dot2.get_center, stroke_opacity=[0, 1], stroke_width=2, stroke_color=YELLOW)

        # current index in y array
        time_step = ValueTracker(0)

        def update_pendulum(mobj):
            idx = int(time_step.get_value())
            
            if idx >= len(x1):
                idx = len(x1) - 1
            
            p1 = origin_point + np.array([x1[idx], y1[idx], 0]) * scale
            p2 = origin_point + np.array([x2[idx], y2[idx], 0]) * scale
            
            rod1.set_points_as_corners([origin_point, p1])
            rod2.set_points_as_corners([p1, p2])
            dot1.move_to(p1)
            dot2.move_to(p2)

        rod1.add_updater(update_pendulum)

        # render constants in top left corner
        const_group = VGroup(
            Text(f"L1: {L1}m", font_size=24),
            Text(f"L2: {L2}m", font_size=24),
            Text(f"M1: {M1}kg", font_size=24),
            Text(f"M2: {M2}kg", font_size=24),
            Text(f"G: {G}m/s²", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(LEFT, buff=-5)

        time_label = Text("Time: ", font_size=24)
        time_display = DecimalNumber(0, num_decimal_places=2, font_size=32)
        timer_group = VGroup(time_label, time_display).arrange(RIGHT).next_to(const_group, DOWN, aligned_edge=LEFT)

        # upd
        time_display.add_updater(
            lambda d: d.set_value(time_step.get_value() * dt)
        )

        # sidebar_bg = BackgroundRectangle(
        #     VGroup(const_group, timer_group), 
        #     buff=0.3, 
        #     fill_opacity=0.2, 
        #     color=GRAY
        # )

        self.add(const_group, timer_group)

        self.add(dot, trace, rod1, rod2, dot1, dot2)
        
        self.play(
            time_step.animate.set_value(len(x1) - 1),
            run_time=t_stop,
            rate_func=linear
        )


class p1(Scene):
    def construct(self):
        self.camera.frame_width = 17.5
        self.camera.frame_height = 10
        
        # constants
        k = 10.0
        m = 1.0
        omega = np.sqrt(k / m)
        initial_x = 1.0
        initial_v = 0.0
        t_max = 12.0
        sim_dt = 0.1
        
        time_points = np.arange(0, t_max + sim_dt, sim_dt)
        x_data = np.zeros(len(time_points))
        v_data = np.zeros(len(time_points))
        
        x_data[0] = initial_x
        v_data[0] = initial_v
        
        for i in range(len(time_points) - 1):
            accel = -(k / m) * x_data[i]
            v_data[i+1] = v_data[i] + accel * sim_dt
            x_data[i+1] = x_data[i] + v_data[i+1] * sim_dt

        wall = Line(UP * 2, DOWN * 2, color=GRAY).move_to(LEFT * 7)
        ground = Line(LEFT * 7.5, RIGHT * 0.5, color=GRAY).move_to(LEFT * 4 + DOWN * 0.5)
        
        block = Square(side_length=1.0, fill_opacity=1, color=BLUE_E).move_to(LEFT * 4)
        spring = ParametricFunction(
            lambda t: np.array([0, 0.2 * np.sin(t * 10 * PI), 0]), 
            t_range=[0, 1], 
            color=WHITE
        )

        def update_spring(m):
            start = wall.get_right()
            end = block.get_center()
            new_spring = ParametricFunction(
                lambda t: np.array([
                    t * (end[0] - start[0]), 
                    0.2 * np.sin(t * 10 * PI), 
                    0
                ]), t_range=[0, 1], color=WHITE
            ).shift(start)
            m.become(new_spring)

        spring.add_updater(update_spring)
        
        animation_group = VGroup(wall, ground, spring, block)

        traj_axes = Axes(
            x_range=[0, 12, 2],
            y_range=[-1.2, 1.2, 0.5],
            x_length=5.5,
            y_length=2.5,
            axis_config={"include_tip": False}
        ).to_corner(UR, buff=1).shift(RIGHT * 5 + UP * 0.5)
        
        traj_title = Tex("Position vs Time").scale(0.8).next_to(traj_axes, UP, buff=0.2)
        traj_points = [traj_axes.c2p(t, x) for t, x in zip(time_points, x_data)]
        traj_line = VMobject().set_points_as_corners(traj_points).set_stroke(width=1.5, color=BLUE_B)
        traj_dot = Dot(color=RED, radius=0.08)

        phase_axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-4, 4, 1],
            x_length=5.5,
            y_length=2.5,
            axis_config={"include_tip": False}
        ).to_corner(DR, buff=1).shift(RIGHT * 5 + DOWN * 0.5)
        
        phase_title = Tex("Phase Space").scale(0.8).next_to(phase_axes, UP, buff=0.2)
        phase_points = [phase_axes.c2p(x, v) for x, v in zip(x_data, v_data)]
        phase_line = VMobject().set_points_as_corners(phase_points).set_stroke(width=1.5, color=BLUE_B)
        phase_dot = Dot(color=RED, radius=0.08)

        self.add(animation_group, traj_axes, traj_title, traj_line, phase_axes, phase_title, phase_line)
        self.add(traj_dot, phase_dot)

        time_tracker = ValueTracker(0)

        block.add_updater(lambda m: m.move_to(LEFT * 4 + RIGHT * np.interp(time_tracker.get_value(), time_points, x_data) * 2))
        
        traj_dot.add_updater(lambda m: m.move_to(
            traj_axes.c2p(time_tracker.get_value(), np.interp(time_tracker.get_value(), time_points, x_data))
        ))
        
        phase_dot.add_updater(lambda m: m.move_to(
            phase_axes.c2p(
                np.interp(time_tracker.get_value(), time_points, x_data),
                np.interp(time_tracker.get_value(), time_points, v_data)
            )
        ))

        self.play(
            time_tracker.animate.set_value(t_max),
            run_time=t_max,
            rate_func=linear
        )
        self.wait(2)


class p12(Scene):
    def construct(self):
        self.camera.frame_width = 17.5
        self.camera.frame_height = 10
        
        g = -9.81
        initial_x = 5.0
        initial_v = 0.0
        t_max = 1.0
        sim_dt = 0.01
        
        time_points = np.arange(0, t_max + sim_dt, sim_dt)
        x_data = np.zeros(len(time_points))
        v_data = np.zeros(len(time_points))
        
        x_data[0] = initial_x
        v_data[0] = initial_v
        
        for i in range(len(time_points) - 1):
            accel = g
            v_data[i+1] = v_data[i] + accel * sim_dt
            x_data[i+1] = x_data[i] + v_data[i+1] * sim_dt

        ground = Line(LEFT * 2, RIGHT * 2, color=GRAY).shift(DOWN * 3.5 + LEFT * 5)
        ruler = DashedLine(UP * 2, DOWN * 3.5, color=GRAY).shift(LEFT * 5)
        
        ball = Dot(radius=0.2, color=BLUE_E).move_to(LEFT * 5 + UP * 2)
        
        traj_axes = Axes(
            x_range=[0, t_max, 0.2],
            y_range=[0, 6, 1],
            x_length=5.5,
            y_length=2.5,
            axis_config={"include_tip": False}
        ).to_corner(UR, buff=1).shift(RIGHT * 5 + UP * 0.5)
        
        traj_title = Tex("Position vs Time").scale(0.8).next_to(traj_axes, UP, buff=0.2)
        traj_points = [traj_axes.c2p(t, x) for t, x in zip(time_points, x_data)]
        traj_line = VMobject().set_points_as_corners(traj_points).set_stroke(width=2, color=BLUE_B)
        traj_dot = Dot(color=RED, radius=0.08)

        phase_axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-12, 2, 2],
            x_length=5.5,
            y_length=2.5,
            axis_config={"include_tip": False}
        ).to_corner(DR, buff=1).shift(RIGHT * 5 + DOWN * 0.5)
        
        phase_title = Tex("Phase Space").scale(0.8).next_to(phase_axes, UP, buff=0.2)
        phase_points = [phase_axes.c2p(x, v) for x, v in zip(x_data, v_data)]
        phase_line = VMobject().set_points_as_corners(phase_points).set_stroke(width=2, color=GREEN_B)
        phase_dot = Dot(color=RED, radius=0.08)

        self.add(ground, ruler, ball, traj_axes, traj_title, traj_line, phase_axes, phase_title, phase_line)
        self.add(traj_dot, phase_dot)

        time_tracker = ValueTracker(0)

        ball.add_updater(lambda m: m.move_to(
            LEFT * 5 + UP * (np.interp(time_tracker.get_value(), time_points, x_data) - 3)
        ))
        
        traj_dot.add_updater(lambda m: m.move_to(
            traj_axes.c2p(time_tracker.get_value(), np.interp(time_tracker.get_value(), time_points, x_data))
        ))
        
        phase_dot.add_updater(lambda m: m.move_to(
            phase_axes.c2p(
                np.interp(time_tracker.get_value(), time_points, x_data),
                np.interp(time_tracker.get_value(), time_points, v_data)
            )
        ))

        self.play(
            time_tracker.animate.set_value(t_max),
            run_time=3,
            rate_func=linear
        )
        self.wait(2)


class p13(Scene):
    def construct(self):
        self.camera.frame_width = 17.5
        self.camera.frame_height = 10
        
        # constants
        GM = 1
        dt = 0.05
        total_steps = 500
        
        vy_tracker = ValueTracker(1)
        time_tracker = ValueTracker(0)
        
        def get_orbit_data(v_init):
            x, y = 1.5, 0.0
            vx, vy = 0.0, v_init
            points = []

            dynamic_steps = int(total_steps * (v_init / 0.8)**2) 
            
            # no idea wtf im doing lowk but works
            for _ in range(max(total_steps, dynamic_steps)):
                r_mag = np.sqrt(x**2 + y**2)
                accel = -GM / (r_mag**3)
                
                vx += accel * x * dt
                vy += accel * y * dt
                x += vx * dt
                y += vy * dt
                
                points.append(np.array([x, y, 0]))
            return points

        moon = Dot(ORIGIN, color=GRAY, radius=0.2)
        moon_label = Text("Moon", font_size=14).next_to(moon, DOWN, buff=-0)
        
        orbit_path = VMobject(color=BLUE)
        orbit_path.add_updater(
            lambda m: m.set_points_as_corners(get_orbit_data(vy_tracker.get_value()))
        )

        satellite = Dot(color=RED, radius=0.1)
        satellite.add_updater(
            lambda s: s.move_to(
                orbit_path.get_points()[int(time_tracker.get_value())]
            )
        )

        v_label = always_redraw(lambda: 
            Text(f"Initial Tangential Velocity = {vy_tracker.get_value():.2f}", font_size=20)
            .to_corner(UL)
        )

        self.add(moon, moon_label, orbit_path, satellite, v_label)

        self.play(time_tracker.animate.set_value(total_steps - 1), run_time=4, rate_func=linear)
        
        self.play(time_tracker.animate.set_value(0), vy_tracker.animate.set_value(0.7), run_time=1)
        self.play(time_tracker.animate.set_value(total_steps - 1), run_time=4, rate_func=linear)
        
        self.play(time_tracker.animate.set_value(0), vy_tracker.animate.set_value(0.82), run_time=1)
        self.play(time_tracker.animate.set_value(total_steps - 1), run_time=4, rate_func=linear)

        self.play(time_tracker.animate.set_value(0), vy_tracker.animate.set_value(1), run_time=1)
        self.play(time_tracker.animate.set_value(total_steps - 1), run_time=4, rate_func=linear)