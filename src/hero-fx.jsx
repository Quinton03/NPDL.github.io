import { createRoot } from 'react-dom/client';
import { SimplexNoise } from '@paper-design/shaders-react';

const REDUCED_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const thesisNoiseProps = {
  colors: ['#c7c8fa', '#4f4dff', '#b6b4b4', '#ff540a', '#ccff00'],
  stepsPerColor: 2,
  softness: 0,
  speed: REDUCED_MOTION ? 0 : 0.2,
  scale: 0.32,
  rotation: 0,
  minPixelRatio: 1,
  maxPixelCount: 640 * 960,
  style: { width: '100%', height: '100%', display: 'block' },
};

function mountThesisNoise(id) {
  const mount = document.getElementById(id);
  if (!mount) return;
  createRoot(mount).render(<SimplexNoise {...thesisNoiseProps} />);
  mount.closest('.thesis-margin')?.classList.add('thesis-margin--ready');
}

mountThesisNoise('thesis-shader-left');
mountThesisNoise('thesis-shader-right');
