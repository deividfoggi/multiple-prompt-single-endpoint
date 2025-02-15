import { DocumentAnalysisClient, AzureKeyCredential } from "@azure/ai-form-recognizer";
import fs from 'fs';

// use your `key` and `endpoint` environment variables
const key = process.env['DI_KEY'];
const endpoint = process.env['DI_ENDPOINT'];

if (!key || !endpoint) {
    console.error("Environment variables DI_KEY and DI_ENDPOINT must be set.");
    process.exit(1);
}

// helper function
function* getTextOfSpans(content, spans) {
    for (const span of spans) {
        yield content.slice(span.offset, span.offset + span.length);
    }
}

export async function runReadScan(filePath) {
    console.log("Starting document analysis...");
    console.log(`Using endpoint: ${endpoint}`);
    console.log(`Using key: ${key ? '****' : 'not set'}`);

    try {
        const client = new DocumentAnalysisClient(endpoint, new AzureKeyCredential(key));
        const fileStream = fs.createReadStream(filePath);
        const poller = await client.beginAnalyzeDocument("prebuilt-read", fileStream);

        const {
            content,
            pages,
            languages,
            styles
        } = await poller.pollUntilDone();

        const result = {
            pages: [],
            languages: [],
            styles: [],
            content: content
        };

        if (pages && pages.length > 0) {
            for (const page of pages) {
                const pageData = {
                    pageNumber: page.pageNumber,
                    unit: page.unit,
                    width: page.width,
                    height: page.height,
                    angle: page.angle,
                    lines: []
                };

                for (const line of page.lines) {
                    const lineData = {
                        content: line.content,
                        words: Array.isArray(line.words) ? line.words.map(word => word.content) : []
                    };
                    pageData.lines.push(lineData);
                }

                result.pages.push(pageData);
            }
        }

        if (languages && languages.length > 0) {
            for (const languageEntry of languages) {
                const languageData = {
                    languageCode: languageEntry.languageCode,
                    confidence: languageEntry.confidence,
                    text: Array.from(getTextOfSpans(content, languageEntry.spans))
                };
                result.languages.push(languageData);
            }
        }

        if (styles.length > 0) {
            for (const style of styles) {
                const styleData = {
                    isHandwritten: style.isHandwritten,
                    confidence: style.confidence,
                    text: Array.from(getTextOfSpans(content, style.spans))
                };
                result.styles.push(styleData);
            }
        }

        console.log("Document analysis completed.");
        return result;
    } catch (error) {
        console.error("Error during document analysis:", error);
        throw error;
    }
}