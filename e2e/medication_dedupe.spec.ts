import { test, expect } from '@playwright/test';

test('medication dedupe', async ({ page }) => {
  await page.goto('/');
  // Placeholder: asumir input texto #med-input y botón #med-add
  const med = 'Aspirina';
  await page.fill('#med-input', med);
  await page.click('#med-add');
  await page.fill('#med-input', med.toLowerCase());
  await page.click('#med-add');
  // Verificación hipotética: lista sin duplicados (#med-list li)
  const items = await page.$$eval('#med-list li', els => els.map(e => e.textContent?.trim()));
  const filtered = items.filter(i => i === med.toLowerCase());
  expect(filtered.length).toBe(1);
});
