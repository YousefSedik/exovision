// create synthetic exoplanet light curve data: baseline + gaussian noise + transit dip(s)
function generateLightCurve({ n = 800, period = 75, transitDepth = 0.015, transitWidth = 3, noise = 0.0015 }) {
  const data = [];
  // time in days (arbitrary units)
  const start = 0;
  const end = 200;
  for (let i = 0; i < n; i++) {
    const t = start + (end - start) * (i / (n - 1));
    // baseline normalized flux near 1.0
    let flux = 1.0;
    // add periodic transits every `period` days
    const phase = (t % period);
    // model transit as a Gaussian-shaped dip centered at phase = period/2
    const center = period / 2;
    const d = Math.exp(-0.5 * Math.pow((phase - center) / transitWidth, 2));
    // subtract scaled dip
    flux -= transitDepth * d;
    // add low-frequency stellar variability (slow sine)
    flux += 0.0025 * Math.sin(2 * Math.PI * t / 120);
    // add gaussian noise
    flux += randn_bm() * noise;
    data.push({ x: t, y: flux });
  }
  return data;
}

// gaussian random helper
function randn_bm() {
  let u = 0, v = 0;
  while (u === 0) u = Math.random();
  while (v === 0) v = Math.random();
  return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
}

const ctx = document.getElementById('fluxChart').getContext('2d');

const initialData = generateLightCurve({});

const fluxChart = new Chart(ctx, {
  type: 'line',

  data: {
    datasets: [{
      label: 'Normalized flux',
      data: initialData,
      showLine: true,
      pointRadius: 0,
      borderWidth: 1,
      tension: 0.05,
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        mode: 'nearest',
        intersect: false,
        callbacks: {
          label: function (context) {
            const x = context.parsed.x.toFixed(3);
            const y = context.parsed.y.toFixed(6);
            return `Time: ${x}  —  Flux: ${y}`;
          }
        }
      },
      zoom: {
        pan: { enabled: false, mode: 'x', modifierKey: 'ctrl' },
        zoom: { wheel: { enabled: false }, pinch: { enabled: false }, mode: 'x' }
      }
    },
    scales: {
      x: {
        type: 'linear',
        title: { display: true, text: 'Time (days)' }
      },
      y: {
        title: { display: true, text: 'Normalized flux' },
        suggestedMin: 1,
        suggestedMax: 1.002
      }
    },
  }
});
