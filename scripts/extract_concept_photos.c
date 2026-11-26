#include <CoreFoundation/CoreFoundation.h>
#include <CoreGraphics/CoreGraphics.h>
#include <ImageIO/ImageIO.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static CFURLRef file_url(const char *path) {
    return CFURLCreateFromFileSystemRepresentation(NULL, (const UInt8 *)path,
                                                   (CFIndex)strlen(path), false);
}

int main(int argc, char **argv) {
    if (argc != 6) {
        fprintf(stderr, "usage: extract_concept_photos source output_dir columns rows prefix\n");
        return 1;
    }
    int columns = atoi(argv[3]), rows = atoi(argv[4]);
    if (columns < 1 || rows < 1) return 1;
    CFURLRef source_url = file_url(argv[1]);
    CGImageSourceRef source = CGImageSourceCreateWithURL(source_url, NULL);
    if (!source) { fprintf(stderr, "cannot open %s\n", argv[1]); return 1; }
    CGImageRef image = CGImageSourceCreateImageAtIndex(source, 0, NULL);
    if (!image) { fprintf(stderr, "cannot decode %s\n", argv[1]); return 1; }
    size_t width = CGImageGetWidth(image) / (size_t)columns;
    size_t height = CGImageGetHeight(image) / (size_t)rows;
    for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
            CGRect frame = CGRectMake(column * width, row * height, width, height);
            CGImageRef crop = CGImageCreateWithImageInRect(image, frame);
            char path[4096];
            snprintf(path, sizeof(path), "%s/%s-%02d.jpg", argv[2], argv[5],
                     row * columns + column + 1);
            CFURLRef destination_url = file_url(path);
            CGImageDestinationRef destination = CGImageDestinationCreateWithURL(
                destination_url, CFSTR("public.jpeg"), 1, NULL);
            if (!crop || !destination) { fprintf(stderr, "cannot create %s\n", path); return 1; }
            CGImageDestinationAddImage(destination, crop, NULL);
            if (!CGImageDestinationFinalize(destination)) {
                fprintf(stderr, "cannot write %s\n", path); return 1;
            }
            CFRelease(destination);
            CFRelease(destination_url);
            CGImageRelease(crop);
        }
    }
    CGImageRelease(image);
    CFRelease(source);
    CFRelease(source_url);
    return 0;
}
