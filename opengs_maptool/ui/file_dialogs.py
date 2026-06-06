from PyQt6.QtWidgets import QFileDialog


def pick_open_image(parent, title):
    path, _ = QFileDialog.getOpenFileName(
        parent, title, "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
    )
    return path or None


def pick_save_image(parent, title):
    """Open save dialog for image files and return path with proper extension."""
    filters = (
        "PNG Files (*.png);;"
        "JPEG Files (*.jpg *.jpeg);;"
        "BMP Files (*.bmp);;"
        "GIF Files (*.gif);;"
        "TIFF Files (*.tiff *.tif);;"
        "WebP Files (*.webp);;"
        "All Files (*)"
    )

    path, selected_filter = QFileDialog.getSaveFileName(parent, title, "", filters)
    if not path:
        return None
    
    # Check if path already has a valid image extension
    lower_path = path.lower()
    if not lower_path.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".tif", ".webp")):
        # Add extension based on selected filter
        if "png" in selected_filter.lower():
            path += ".png"
        elif "jpeg" in selected_filter.lower():
            path += ".jpg"
        elif "bmp" in selected_filter.lower():
            path += ".bmp"
        elif "gif" in selected_filter.lower():
            path += ".gif"
        elif "tiff" in selected_filter.lower():
            path += ".tiff"
        elif "webp" in selected_filter.lower():
            path += ".webp"
        else:
            path += ".png"
    
    return path


def pick_save_data(parent, title):
    """Open save dialog for data files and return (path, format) tuple with proper extension."""
    filters = (
        "JSON Files (*.json);;"
        "CSV Files (*.csv);;"
        "YAML Files (*.yaml *.yml);;"
        "XML Files (*.xml);;"
        "All Files (*)"
    )

    path, selected_filter = QFileDialog.getSaveFileName(parent, title, "", filters)
    if not path:
        return None, None

    lower_path = path.lower()
    
    # Determine format from extension
    if lower_path.endswith(".json"):
        fmt = "json"
    elif lower_path.endswith(".csv"):
        fmt = "csv"
    elif lower_path.endswith((".yaml", ".yml")):
        fmt = "yaml"
    elif lower_path.endswith(".xml"):
        fmt = "xml"
    else:
        # No valid extension, add one based on selected filter
        if "json" in selected_filter.lower():
            fmt = "json"
            path += ".json"
        elif "yaml" in selected_filter.lower():
            fmt = "yaml"
            path += ".yaml"
        elif "xml" in selected_filter.lower():
            fmt = "xml"
            path += ".xml"
        elif "csv" in selected_filter.lower():
            fmt = "csv"
            path += ".csv"
        else:
            # Default to JSON
            fmt = "json"
            path += ".json"
    
    return path, fmt
