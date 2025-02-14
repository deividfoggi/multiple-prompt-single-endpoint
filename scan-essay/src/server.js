import express from 'express';
import { static as expressStatic } from 'express';
import multer from 'multer';
import { join } from 'path';
import { runReadScan } from './readScan.js';
import { createProxyMiddleware } from 'http-proxy-middleware';

const app = express();
const PORT = process.env.PORT || 8080;
const OpenAIEndpoint = process.env.OPENAI_ENDPOINT;
app.use(expressStatic(join(__dirname, '../public')));
const upload = multer({ dest: 'uploads/' });

app.get('/scan', async (res) => {
    try {
        res.sendFile(join(__dirname, '../public/index.html'));
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});

app.post('/upload', upload.single('file'), async (req, res) => {
    const filePath = req.file.path;
    try {
        const result = await runReadScan(filePath);
        res.json(result);
    } catch (error) {
        res.status(500).send('Error analyzing document');
    }
});

app.use('/api', (next) => {
    console.log('Received request for /api');
    next();
});

app.use('/api', createProxyMiddleware({
    target: OpenAIEndpoint,
    changeOrigin: true,
    pathRewrite: {
        '^/api': '/score'
    }
}));

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});