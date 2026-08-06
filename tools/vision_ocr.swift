// Japanese OCR for the rasterised dialogue in refs/JLPT_N2_NEW/ script PDFs.
//
// Most of those PDFs draw their dialogue as 1-bit stencil bitmaps rather than
// text, so no PDF text extractor can reach it. This wraps Apple's Vision
// recognizer (built into macOS, no install, good at vertical-ruby Japanese) and
// prints one TSV row per recognised line:
//
//     x0 <TAB> top <TAB> x1 <TAB> bottom <TAB> confidence <TAB> text
//
// Coordinates are normalised to 0..1 with a TOP-LEFT origin, so the caller can
// scale them straight onto PDF points and merge with the real text layer.
// Called by tools/extract_jlpt_n2_new.py, which builds it on first use.

import Foundation
import Vision
import AppKit

let paths = Array(CommandLine.arguments.dropFirst())
guard !paths.isEmpty else {
    FileHandle.standardError.write("usage: vision_ocr <page.png> [...]\n".data(using: .utf8)!)
    exit(2)
}

for path in paths {
    // One "--- file ---" line per input keeps multi-page batches unambiguous.
    print("--- \(path) ---")
    guard let image = NSImage(contentsOfFile: path),
          let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        FileHandle.standardError.write("cannot read image: \(path)\n".data(using: .utf8)!)
        continue
    }

    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages = ["ja-JP", "en-US"]
    // Language correction rewrites toward everyday prose, which is exactly the
    // wrong prior for exam text full of proper nouns and clipped speech.
    request.usesLanguageCorrection = false

    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    do {
        try handler.perform([request])
    } catch {
        FileHandle.standardError.write("OCR failed for \(path): \(error)\n".data(using: .utf8)!)
        continue
    }

    let observations = request.results ?? []
    let ordered = observations.sorted { a, b in
        // Reading order: top to bottom, then left to right within a line.
        if abs(a.boundingBox.midY - b.boundingBox.midY) > 0.006 {
            return a.boundingBox.midY > b.boundingBox.midY
        }
        return a.boundingBox.minX < b.boundingBox.minX
    }
    for observation in ordered {
        guard let best = observation.topCandidates(1).first else { continue }
        let box = observation.boundingBox           // origin bottom-left
        let top = 1.0 - box.maxY                    // flip to top-left origin
        let bottom = 1.0 - box.minY
        let text = best.string.replacingOccurrences(of: "\t", with: " ")
        print(String(format: "%.5f\t%.5f\t%.5f\t%.5f\t%.3f\t%@",
                     box.minX, top, box.maxX, bottom, best.confidence, text))
    }
}
