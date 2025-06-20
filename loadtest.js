import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Taux d’erreur
export let errorRate = new Rate('errors');

export let options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m',  target: 10 },
    { duration: '30s', target: 0  },
  ],
  thresholds: {
    errors: ['rate<0.1'],           // < 10% d’erreurs
    http_req_duration: ['p(95)<500'], // 95% < 500ms
  },
};

//const BASE_URL = 'http://127.0.0.1:8001/api/v1';
//const BASE_URL = 'http://127.0.0.1:8080/api/v1';
const BASE_URL = 'http://127.0.0.1:8080/api/v1';


const AUTH = {
  headers: {
    // ** Choisis la ligne qui correspond à ton API ** 
    'Authorization': 'token1',            
    // ou si Bearer est requis
    // 'Authorization': 'Bearer token1',
    'Content-Type': 'application/json',
  },
};

export default function () {
  // 1) stock
  let storeId = Math.floor(Math.random() * 5) + 1;
  let r1 = http.get(`${BASE_URL}/stores/${storeId}/stock`, AUTH);
  check(r1, { 'stock 200': r => r.status === 200 }) || errorRate.add(1);

  // 2) rapport
  let start = '2025-06-01', end = '2025-06-15';
  let r2 = http.get(`${BASE_URL}/reports/sales?start=${start}&end=${end}`, AUTH);
  check(r2, { 'report 200': r => r.status === 200 }) || errorRate.add(1);

  // 3) dashboard
  let r3 = http.get(`${BASE_URL}/dashboard/`, AUTH);
  check(r3, { 'dashboard 200': r => r.status === 200 }) || errorRate.add(1);

  sleep(1);
}
