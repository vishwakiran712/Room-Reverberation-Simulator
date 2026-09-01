import sys
import numpy as np

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QDoubleSpinBox, QComboBox, QGroupBox,
    QFrame, QSplitter, QScrollArea, QTabWidget
)
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# -------------------------------------------------------------------------
# Custom Styling (CSS)
# -------------------------------------------------------------------------
DARK_STYLE = """
QMainWindow {
    background-color: #0D1117;
}
QWidget {
    color: #C9D1D9;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 11px;
}
QGroupBox {
    border: 1px solid #21262D;
    border-radius: 6px;
    margin-top: 10px;
    font-weight: bold;
    color: #58A6FF;
    background-color: #161B22;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 8px;
    background-color: #161B22;
    border-radius: 3px;
}
QLabel {
    color: #8B949E;
}
QDoubleSpinBox, QComboBox {
    background-color: #0D1117;
    border: 1px solid #30363D;
    border-radius: 4px;
    padding: 4px 6px;
    color: #58A6FF;
    font-weight: bold;
}
QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #58A6FF;
}
QComboBox QAbstractItemView {
    background-color: #161B22;
    selection-background-color: #21262D;
    color: #C9D1D9;
}
QFrame#metricCard {
    background-color: #0D1117;
    border: 1px solid #21262D;
    border-radius: 6px;
}
QTabWidget::pane {
    border: 1px solid #21262D;
    background-color: #161B22;
    border-radius: 4px;
}
QTabBar::tab {
    background: #0D1117;
    border: 1px solid #21262D;
    padding: 6px 12px;
    color: #8B949E;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QTabBar::tab:selected {
    background: #161B22;
    color: #58A6FF;
    border-bottom-color: #161B22;
    font-weight: bold;
}
"""

# Presets configuration dictionary
PRESETS = {
    "Custom": None,
    "Small Bedroom": {"length": 4.0, "width": 3.0, "height": 2.5, "wall_a": 0.20, "ceiling_a": 0.15, "floor_a": 0.40, "dist": 1.5},
    "Office": {"length": 6.0, "width": 4.5, "height": 2.8, "wall_a": 0.15, "ceiling_a": 0.60, "floor_a": 0.25, "dist": 2.0},
    "Classroom": {"length": 9.0, "width": 7.0, "height": 3.2, "wall_a": 0.12, "ceiling_a": 0.50, "floor_a": 0.15, "dist": 3.0},
    "Studio": {"length": 5.5, "width": 4.0, "height": 2.8, "wall_a": 0.65, "ceiling_a": 0.70, "floor_a": 0.45, "dist": 1.8},
    "Hall": {"length": 25.0, "width": 15.0, "height": 8.0, "wall_a": 0.08, "ceiling_a": 0.10, "floor_a": 0.05, "dist": 8.0}
}

class RoomReverberationSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Room Reverberation Simulator")
        self.resize(1300, 840)
        self.setMinimumSize(1000, 680)

        self.fs = 44100  # Sample rate (Hz)
        self.c = 343.0   # Speed of sound (m/s)

        # State storage
        self.volume = 0.0
        self.surface_area = 0.0
        self.sabins = 0.0
        self.avg_absorption = 0.0
        self.rt60 = 0.0

        self.t = None
        self.rir = None
        self.edc_db = None

        self.is_updating_preset = False

        self.init_ui()
        self.load_preset("Small Bedroom")

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # =================================---------------------------------
        # LEFT PANEL: Presets & Room Configuration Controls
        # =================================---------------------------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        ctrl_layout = QVBoxLayout(scroll_content)

        # 1. Presets Selector
        group_preset = QGroupBox("PRESETS")
        layout_preset = QVBoxLayout(group_preset)
        self.combo_presets = QComboBox()
        self.combo_presets.addItems(list(PRESETS.keys()))
        self.combo_presets.currentTextChanged.connect(self.on_preset_changed)
        layout_preset.addWidget(self.combo_presets)
        ctrl_layout.addWidget(group_preset)

        # 2. Geometry & Distance Controls
        group_geo = QGroupBox("1. ROOM GEOMETRY & DISTANCE")
        grid_geo = QGridLayout(group_geo)
        grid_geo.setSpacing(6)

        grid_geo.addWidget(QLabel("Length (m):"), 0, 0)
        self.spin_length = QDoubleSpinBox()
        self.spin_length.setRange(1.0, 50.0)
        self.spin_length.setSingleStep(0.5)
        grid_geo.addWidget(self.spin_length, 0, 1)

        grid_geo.addWidget(QLabel("Width (m):"), 1, 0)
        self.spin_width = QDoubleSpinBox()
        self.spin_width.setRange(1.0, 50.0)
        self.spin_width.setSingleStep(0.5)
        grid_geo.addWidget(self.spin_width, 1, 1)

        grid_geo.addWidget(QLabel("Height (m):"), 2, 0)
        self.spin_height = QDoubleSpinBox()
        self.spin_height.setRange(1.0, 20.0)
        self.spin_height.setSingleStep(0.2)
        grid_geo.addWidget(self.spin_height, 2, 1)

        grid_geo.addWidget(QLabel("Source-Listener Dist (m):"), 3, 0)
        self.spin_dist = QDoubleSpinBox()
        self.spin_dist.setRange(0.1, 50.0)
        self.spin_dist.setSingleStep(0.2)
        grid_geo.addWidget(self.spin_dist, 3, 1)

        ctrl_layout.addWidget(group_geo)

        # 3. Surface Absorption Coefficients
        group_abs = QGroupBox("2. SURFACE ABSORPTION COEFFICIENTS (α)")
        grid_abs = QGridLayout(group_abs)
        grid_abs.setSpacing(6)

        grid_abs.addWidget(QLabel("Wall Absorption:"), 0, 0)
        self.spin_wall_a = QDoubleSpinBox()
        self.spin_wall_a.setRange(0.01, 0.99)
        self.spin_wall_a.setSingleStep(0.05)
        grid_abs.addWidget(self.spin_wall_a, 0, 1)

        grid_abs.addWidget(QLabel("Ceiling Absorption:"), 1, 0)
        self.spin_ceiling_a = QDoubleSpinBox()
        self.spin_ceiling_a.setRange(0.01, 0.99)
        self.spin_ceiling_a.setSingleStep(0.05)
        grid_abs.addWidget(self.spin_ceiling_a, 1, 1)

        grid_abs.addWidget(QLabel("Floor Absorption:"), 2, 0)
        self.spin_floor_a = QDoubleSpinBox()
        self.spin_floor_a.setRange(0.01, 0.99)
        self.spin_floor_a.setSingleStep(0.05)
        grid_abs.addWidget(self.spin_floor_a, 2, 1)

        ctrl_layout.addWidget(group_abs)
        ctrl_layout.addStretch()

        scroll.setWidget(scroll_content)
        left_layout.addWidget(scroll)

        # Connect signals for real-time recalculation
        for spin in [self.spin_length, self.spin_width, self.spin_height,
                     self.spin_dist, self.spin_wall_a, self.spin_ceiling_a, self.spin_floor_a]:
            spin.valueChanged.connect(self.on_param_changed)

        # =================================---------------------------------
        # RIGHT PANEL: Calculated Results & Matplotlib Display
        # =================================---------------------------------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Calculated Acoustic Indicators Grid
        metrics_group = QGroupBox("CALCULATED ACOUSTIC PARAMETERS")
        grid_metrics = QGridLayout(metrics_group)
        grid_metrics.setSpacing(6)

        self.lbl_volume = self.create_metric_card("Room Volume", "0.0 m³", grid_metrics, 0, 0)
        self.lbl_surface = self.create_metric_card("Surface Area", "0.0 m²", grid_metrics, 0, 1)
        self.lbl_sabins = self.create_metric_card("Total Absorption", "0.0 Sabins", grid_metrics, 0, 2)

        self.lbl_avg_a = self.create_metric_card("Avg Absorption (a_avg)", "0.00", grid_metrics, 1, 0)
        self.lbl_rt60 = self.create_metric_card("Sabine RT60", "0.00 s", grid_metrics, 1, 1)

        # Highlight RT60 metric card
        self.lbl_rt60.setStyleSheet("color: #3FB950; font-size: 14px; font-weight: bold;")

        right_layout.addWidget(metrics_group)

        # Matplotlib Display Canvas Layout
        plots_group = QGroupBox("ROOM VISUALIZATION & ACOUSTIC RESPONSE")
        layout_plots = QVBoxLayout(plots_group)

        self.fig = Figure(figsize=(9, 7), facecolor='#161B22')
        self.canvas = FigureCanvas(self.fig)
        layout_plots.addWidget(self.canvas)

        right_layout.addWidget(plots_group, stretch=1)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([360, 940])

    def create_metric_card(self, title, default_val, layout, row, col):
        card = QFrame()
        card.setObjectName("metricCard")
        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(6, 4, 6, 4)

        lbl_title = QLabel(title.upper())
        lbl_title.setStyleSheet("color: #8B949E; font-size: 10px; font-weight: bold;")
        lbl_val = QLabel(default_val)
        lbl_val.setStyleSheet("color: #58A6FF; font-size: 13px; font-weight: bold;")

        vbox.addWidget(lbl_title)
        vbox.addWidget(lbl_val)
        layout.addWidget(card, row, col)
        return lbl_val

    def on_preset_changed(self, preset_name):
        if preset_name in PRESETS and PRESETS[preset_name] is not None:
            self.load_preset(preset_name)

    def load_preset(self, preset_name):
        data = PRESETS[preset_name]
        if data is None:
            return

        self.is_updating_preset = True

        self.spin_length.setValue(data["length"])
        self.spin_width.setValue(data["width"])
        self.spin_height.setValue(data["height"])
        self.spin_wall_a.setValue(data["wall_a"])
        self.spin_ceiling_a.setValue(data["ceiling_a"])
        self.spin_floor_a.setValue(data["floor_a"])
        self.spin_dist.setValue(data["dist"])

        self.is_updating_preset = False
        self.process_pipeline()

    def on_param_changed(self):
        if not self.is_updating_preset:
            self.combo_presets.blockSignals(True)
            self.combo_presets.setCurrentText("Custom")
            self.combo_presets.blockSignals(False)
        self.process_pipeline()

    def calculate_sabine_rt60(self):
        """Calculates Volume, Surface Area, Sabins, and Sabine RT60."""
        L = self.spin_length.value()
        W = self.spin_width.value()
        H = self.spin_height.value()

        # Surface Areas
        s_floor = L * W
        s_ceiling = L * W
        s_walls = 2 * (L * H + W * H)

        self.surface_area = s_floor + s_ceiling + s_walls
        self.volume = L * W * H

        a_wall = self.spin_wall_a.value()
        a_ceiling = self.spin_ceiling_a.value()
        a_floor = self.spin_floor_a.value()

        # Total Absorption in Sabins (m^2)
        self.sabins = (s_walls * a_wall) + (s_ceiling * a_ceiling) + (s_floor * a_floor)
        self.avg_absorption = self.sabins / max(1e-6, self.surface_area)

        # Sabine Equation: RT60 = 0.161 * V / A
        if self.sabins > 1e-4:
            self.rt60 = 0.161 * self.volume / self.sabins
        else:
            self.rt60 = 0.0

        # Update Indicators UI
        self.lbl_volume.setText(f"{self.volume:.1f} m³")
        self.lbl_surface.setText(f"{self.surface_area:.1f} m²")
        self.lbl_sabins.setText(f"{self.sabins:.1f} Sabins")
        self.lbl_avg_a.setText(f"{self.avg_absorption:.2f}")
        self.lbl_rt60.setText(f"{self.rt60:.2f} s")

    def generate_impulse_response(self):
        """Generates synthetic impulse response based on room parameters."""
        duration = max(1.0, self.rt60 * 1.3)
        num_samples = int(self.fs * duration)
        self.t = np.linspace(0, duration, num_samples, endpoint=False)

        dist = min(self.spin_dist.value(), np.sqrt(self.spin_length.value()**2 + self.spin_width.value()**2))
        
        # 1. Direct Sound
        direct_delay_s = dist / self.c
        direct_idx = int(direct_delay_s * self.fs)

        self.rir = np.zeros(num_samples)
        if direct_idx < num_samples:
            # Direct sound amplitude inverse to distance
            self.rir[direct_idx] = 1.0 / max(1.0, dist)

        # 2. Early Reflections
        # Approximate 1st and 2nd order reflections
        reflect_coeff = np.sqrt(1.0 - self.avg_absorption)
        num_reflections = 12
        np.random.seed(42)  # Deterministic seed for smooth interactive updates

        early_end_s = direct_delay_s + 0.08  # 80ms window
        early_end_idx = min(num_samples, int(early_end_s * self.fs))

        if early_end_idx > direct_idx + 1:
            ref_indices = np.random.randint(direct_idx + 1, early_end_idx, num_reflections)
            for idx in ref_indices:
                delay_t = self.t[idx] - direct_delay_s
                path_dist = dist + (delay_t * self.c)
                amp = (reflect_coeff ** 2) / max(1.0, path_dist) * np.random.choice([-1, 1])
                self.rir[idx] += amp

        # 3. Late Exponential Reverberation Decay
        tau = max(0.01, self.rt60 / (3.0 * np.log(10)))  # Decay rate for 60 dB drop
        decay_envelope = np.zeros(num_samples)

        if direct_idx + 1 < num_samples:
            t_decay = self.t[direct_idx + 1:] - direct_delay_s
            decay_envelope[direct_idx + 1:] = np.exp(-t_decay / tau)

        noise = np.random.normal(0, 0.05, num_samples)
        self.rir += noise * decay_envelope * reflect_coeff

        # 4. Energy Decay Curve (EDC) via Schroeder Integration
        h2 = self.rir ** 2
        schroeder = np.flip(np.cumsum(np.flip(h2)))
        max_e = max(1e-12, schroeder[0])
        self.edc_db = 10 * np.log10(np.maximum(1e-12, schroeder / max_e))

    def process_pipeline(self):
        self.calculate_sabine_rt60()
        self.generate_impulse_response()
        self.plot_all()

    def plot_all(self):
        self.fig.clear()

        grid_c = '#21262D'
        text_c = '#8B949E'

        # 1. Subplot 1: Room Geometry Diagram
        ax1 = self.fig.add_subplot(221)
        ax1.set_facecolor('#0D1117')

        L = self.spin_length.value()
        W = self.spin_width.value()
        dist = min(self.spin_dist.value(), np.sqrt(L**2 + W**2))

        # Draw room boundary
        rect = matplotlib.patches.Rectangle((0, 0), L, W, linewidth=1.5, edgecolor='#58A6FF', facecolor='#161B22')
        ax1.add_patch(rect)

        # Source and Listener Positions
        src_pos = (L * 0.3, W * 0.5)
        lst_x = min(L * 0.9, src_pos[0] + dist)
        lst_pos = (lst_x, W * 0.5)

        ax1.plot(src_pos[0], src_pos[1], 'ro', markersize=8, label="Source")
        ax1.plot(lst_pos[0], lst_pos[1], 'go', markersize=8, label="Listener")

        # Direct path arrow
        ax1.annotate("", xy=lst_pos, xytext=src_pos,
                     arrowprops=dict(arrowstyle="->", color='#3FB950', lw=1.5))

        # Reflection path illustration
        wall_pts = [(L * 0.5, W), (L * 0.5, 0)]
        for pt in wall_pts:
            ax1.plot([src_pos[0], pt[0], lst_pos[0]], [src_pos[1], pt[1], lst_pos[1]],
                     '--', color='#F0883E', alpha=0.6, linewidth=1.0)

        ax1.set_xlim([-0.5, L + 0.5])
        ax1.set_ylim([-0.5, W + 0.5])
        ax1.set_aspect('equal')
        ax1.set_title("Room Layout (2D Schematic)", color='#58A6FF', fontsize=9, fontweight='bold', loc='left')
        ax1.set_xlabel("Length (m)", color=text_c, fontsize=8)
        ax1.set_ylabel("Width (m)", color=text_c, fontsize=8)
        ax1.tick_params(colors=text_c, labelsize=7)
        ax1.grid(True, linestyle='--', alpha=0.3, color=grid_c)
        ax1.legend(facecolor='#161B22', edgecolor=grid_c, labelcolor=text_c, fontsize=7, loc='upper right')

        # 2. Subplot 2: Direct Sound & Early Reflections Detail
        ax2 = self.fig.add_subplot(222)
        ax2.set_facecolor('#0D1117')

        t_ms = self.t * 1000.0
        early_mask = t_ms <= (dist / self.c * 1000.0 + 80.0)

        ax2.stem(t_ms[early_mask], self.rir[early_mask], linefmt='#58A6FF', markerfmt='o', basefmt=" ")
        ax2.set_title("Direct Sound & Early Reflections", color='#58A6FF', fontsize=9, fontweight='bold', loc='left')
        ax2.set_xlabel("Time (ms)", color=text_c, fontsize=8)
        ax2.set_ylabel("Amplitude", color=text_c, fontsize=8)
        ax2.tick_params(colors=text_c, labelsize=7)
        ax2.grid(True, linestyle='--', alpha=0.3, color=grid_c)

        # 3. Subplot 3: Complete Synthetic Impulse Response
        ax3 = self.fig.add_subplot(223)
        ax3.set_facecolor('#0D1117')

        ax3.plot(t_ms, self.rir, color='#3FB950', linewidth=0.8, alpha=0.8)
        ax3.set_title("Full Synthetic Impulse Response h(t)", color='#3FB950', fontsize=9, fontweight='bold', loc='left')
        ax3.set_xlabel("Time (ms)", color=text_c, fontsize=8)
        ax3.set_ylabel("Amplitude", color=text_c, fontsize=8)
        ax3.tick_params(colors=text_c, labelsize=7)
        ax3.grid(True, linestyle='--', alpha=0.3, color=grid_c)

        # 4. Subplot 4: Energy Decay Curve (EDC)
        ax4 = self.fig.add_subplot(224)
        ax4.set_facecolor('#0D1117')

        ax4.plot(t_ms, self.edc_db, color='#F0883E', linewidth=1.5, label="Energy Decay (Schroeder)")
        ax4.axhline(y=-60, color='#F85149', linestyle=':', label="RT60 Threshold (-60 dB)")

        ax4.set_ylim([-80, 5])
        ax4.set_title("Energy Decay Curve", color='#F0883E', fontsize=9, fontweight='bold', loc='left')
        ax4.set_xlabel("Time (ms)", color=text_c, fontsize=8)
        ax4.set_ylabel("Energy Decay (dB)", color=text_c, fontsize=8)
        ax4.tick_params(colors=text_c, labelsize=7)
        ax4.grid(True, linestyle='--', alpha=0.3, color=grid_c)
        ax4.legend(facecolor='#161B22', edgecolor=grid_c, labelcolor=text_c, fontsize=7, loc='upper right')

        for ax in [ax1, ax2, ax3, ax4]:
            for spine in ax.spines.values():
                spine.set_color(grid_c)

        self.fig.tight_layout()
        self.canvas.draw()


# -------------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(DARK_STYLE)

    window = RoomReverberationSimulatorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()