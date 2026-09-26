def contrast_ratio(foreground, background):
    def channel(value):
        return value / 255

    def luminance(color):
        red, green, blue = color
        return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)

    lighter = max(luminance(foreground), luminance(background))
    darker = min(luminance(foreground), luminance(background))
    return (lighter + 0.05) / (darker + 0.05)
