const express = require('express');
const axios = require('axios');

const API_TOKEN = 'eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg';

const httpsAgent = new (require('https').Agent)({ rejectUnauthorized: false });

const app = express();
app.use(express.json());

async function getCompanyId(companyName) {
    const url = `https://downdetectorapi.com/v2/companies/search?fields=id,name,slug,country_iso,indicators,site_id&name=${companyName}`;
    const headers = { Authorization: `Bearer ${API_TOKEN}` };

    try {
        const response = await axios.get(url, { headers, httpsAgent });
        const companies = response.data;

        if (companies && companies.length > 0) {
            for (const company of companies) {
                if (company.country_iso === 'CO') {  // Solo toma compañías de Colombia
                    console.log(`Company found: ${company.name} with ID: ${company.id}`);
                    return company.id;
                }
            }
        } else {
            console.log(`No companies found for name: ${companyName}`);
        }
    } catch (error) {
        console.error(`Error ${error.response?.status}: ${error.response?.data}`);
    }
    return null;
}

// Endpoint para obtener los términos de tweet
app.post('/getTweetTerms', async (req, res) => {
    const { startDate, endDate, filter, exclude, amount, companyName } = req.body;

    if (!startDate || !endDate || !companyName) {
        return res.status(400).json({ error: "Fechas y nombre de la compañía son requeridos" });
    }

    try {
        const companyId = await getCompanyId(companyName);
        if (!companyId) {
            return res.status(404).json({ error: "No se encontró la compañía con el nombre especificado" });
        }

        const url = `https://downdetectorapi.com/v2/companies/${companyId}/tweets/terms`;
        const params = {
            startdate: startDate,
            enddate: endDate,
            filter: filter,
            exclude: exclude || 'comcast,my-term,.*my.regexp.*',
            amount: amount || '25',
        };
        const headers = { Authorization: `Bearer ${API_TOKEN}` };

        const response = await axios.get(url, { headers, params, httpsAgent });
        return res.status(200).json(response.data);
    } catch (error) {
        console.error(`Error ${error.response?.status}: ${error.response?.data}`);
        return res.status(500).json({ error: "Error obteniendo términos de tweets" });
    }
});

// Inicializar el servidor en el puerto 3000
app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
