const axios = require('axios');

// Token de API de Downdetector
const API_TOKEN = 'eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg';

// Configuración para ignorar la verificación de certificado
const httpsAgent = new (require('https').Agent)({ rejectUnauthorized: false });

// Función para obtener el company_id de una compañía
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
        console.error(`Error ${error.response.status}: ${error.response.data}`);
    }
    return null;
}

// Función para obtener tweets de la compañía usando el company_id
async function getCompanyTweets(companyId, startDate, endDate, pageSize = 25) {
    const url = `https://downdetectorapi.com/v2/companies/${companyId}/tweets`;
    const params = {
        startdate: startDate,
        enddate: endDate,
        page_size: pageSize.toString(),
        term: ["servicio, problemas, internet"],
        retweets: "true"
    };
    const headers = { Authorization: `Bearer ${API_TOKEN}` };

    try {
        const response = await axios.get(url, { headers, params, httpsAgent });
        const tweets = response.data;

        if (Array.isArray(tweets)) {
            // Si la respuesta es una lista
            console.log(`Tweets encontrados para company_id ${companyId}:`);
            tweets.forEach(tweet => console.log(tweet));
        } else if (typeof tweets === 'object' && tweets.data) {
            // Si la respuesta es un diccionario (como se esperaba)
            console.log(`Tweets encontrados para company_id ${companyId}:`);
            tweets.data.forEach(tweet => console.log(tweet));
        } else {
            console.log(`Formato de respuesta inesperado para company_id ${companyId}.`);
        }
    } catch (error) {
        console.error(`Error ${error.response.status}: ${error.response.data}`);
    }
}

// Ejecución de las funciones para un ejemplo
(async () => {
    const companyName = "Claro";
    const startDate = "2024-11-05T00:00:00+00:00";
    const endDate = "2024-11-07T00:00:00+00:00";

    // Obtener el company_id
    const companyId = await getCompanyId(companyName);

    // Si se encuentra el company_id, obtenemos los tweets
    if (companyId) {
        await getCompanyTweets(companyId, startDate, endDate);
    }
})();
