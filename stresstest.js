import http from 'k6/http';
import { check, sleep } from 'k6';


export let options = {
  stages: [
    // on part de 0 VUs et on monte à 50 VUs en 1 minute
    { duration: '1m', target: 50 },
    // on continue la montée jusqu'à 200 VUs en 4 minutes
    { duration: '4m', target: 200 },
    // on maintient 200 VUs pendant 2 minutes
    { duration: '2m', target: 200 },
    // enfin on redescend sur 0 VUs en 1m
    { duration: '1m', target: 0 },
  ],
  thresholds: {
    // on enregistre le 95e percentile de la latence
    'http_req_duration': ['p(95)<1000'], 
    // mais on ne coupe pas le test en cas d’erreurs
    // on va observer quand le taux d’erreurs grimpe
  },
};

//const BASE_URL = 'http://127.0.0.1:8001/api/v1';
const BASE_URL = 'http://127.0.0.1:8080/api/v1';

const AUTH = { headers: { 'Authorization': 'token1', 'Content-Type': 'application/json' } };

export default function () {
  // ton même workflow en 4 étapes
  let storeId = Math.floor(Math.random() * 5) + 1;
  let res1 = http.get(`${BASE_URL}/stores/${storeId}/stock`, AUTH);
  check(res1, { 'stock 200': r => r.status === 200 });

  let start = '2025-06-01', end = '2025-06-15';
  let res2 = http.get(`${BASE_URL}/reports/sales?start=${start}&end=${end}`, AUTH);
  check(res2, { 'report 200': r => r.status === 200 });

  let prodId = Math.floor(Math.random() * 5) + 1;
  let payload = JSON.stringify({ nom: `Stress-${prodId}`, prix: Math.random() * 100 });
  let res3 = http.put(`${BASE_URL}/products/${prodId}`, payload, AUTH);
  check(res3, { 'update 200': r => r.status === 200 });

  let res4 = http.get(`${BASE_URL}/dashboard/`, AUTH);
  check(res4, { 'dashboard 200': r => r.status === 200 });

  sleep(1);
}
