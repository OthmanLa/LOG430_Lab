import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10,              // 10 utilisateurs simultanés
  duration: '20s',      // pendant 20 secondes
};

export default function () {
  const res = http.get('http://localhost:8000/produits', {
    headers: {
      'apikey': 'token1'
    }
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  sleep(1); // Pause de 1s entre les requêtes
}
