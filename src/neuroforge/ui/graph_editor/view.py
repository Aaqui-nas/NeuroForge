from __future__ import annotations

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent, QPainter, QTransform, QWheelEvent
from PySide6.QtWidgets import QGraphicsView

from .scene import GraphScene

ZOOM_FACTOR = 1.15
ZOOM_MIN = 0.1
ZOOM_MAX = 10.0


class GraphView(QGraphicsView):
    """Viewport for the graph editor scene.

    Supports zoom via the mouse wheel and pan via the middle mouse button.
    Zoom is clamped to [`ZOOM_MIN`, `ZOOM_MAX`] and anchored under the
    cursor so the point under the mouse stays fixed during zoom.

    Attributes:
        ZOOM_FACTOR: Multiplicative step applied per wheel tick.
        ZOOM_MIN: Minimum allowed zoom level (most zoomed-out).
        ZOOM_MAX: Maximum allowed zoom level (most zoomed-in).
    """

    def __init__(self, scene: GraphScene) -> None:
        """Create the view and configure rendering.

        Args:
            scene: The `GraphScene` to display.
        """
        super().__init__(scene)
        self._zoom: float = 1.0
        self._panning: bool = False
        self._pan_start: QPoint | None = None

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Zoom in or out under the cursor on wheel scroll."""
        if event.angleDelta().y() > 0:
            self._apply_zoom(ZOOM_FACTOR)
        else:
            self._apply_zoom(1.0 / ZOOM_FACTOR)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Start panning on middle-mouse-button press."""
        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = True
            self._pan_start = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Pan the view when the middle mouse button is held."""
        if self._panning and self._pan_start is not None:
            delta = event.pos() - self._pan_start
            self._pan_start = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """End panning on middle-mouse-button release."""
        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = False
            self._pan_start = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def zoom_in(self) -> None:
        """Zoom in by one step (`ZOOM_FACTOR`)."""
        self._apply_zoom(ZOOM_FACTOR)

    def zoom_out(self) -> None:
        """Zoom out by one step (``1 / ZOOM_FACTOR``)."""
        self._apply_zoom(1.0 / ZOOM_FACTOR)

    def zoom_reset(self) -> None:
        """Reset zoom to 1:1 (identity transform)."""
        self._zoom = 1.0
        self.setTransform(QTransform())

    def fit_view(self) -> None:
        """Fit all scene items into the viewport, preserving aspect ratio."""
        scene = self.scene()
        if scene is not None:
            self.fitInView(scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def _apply_zoom(self, factor: float) -> None:
        """Scale the view by *factor*, clamped to [`ZOOM_MIN`, `ZOOM_MAX`].

        Args:
            factor: Multiplicative zoom factor (>1 zooms in, <1 zooms out).
        """
        new_zoom = self._zoom * factor
        new_zoom = max(ZOOM_MIN, min(ZOOM_MAX, new_zoom))
        actual_factor = new_zoom / self._zoom
        self._zoom = new_zoom
        self.scale(actual_factor, actual_factor)
