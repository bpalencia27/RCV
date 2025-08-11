import { test, expect } from '@playwright/test';

// Asegura que la generación de informe via preview se muestre y contenga el prompt
// Asume que la app Reflex corre en http://localhost:3000 (ajustar baseURL en config si distinto)

test('generar informe preview', async ({ page }) => {
  await page.goto('/');
  // Llenar campos mínimos
  await page.getByLabel('Nombre Completo').fill('Paciente Demo');
  await page.getByLabel('Edad (años)').fill('55');
  await page.getByLabel('Sexo').selectOption('m');
  await page.getByLabel('Creatinina (mg/dL)').fill('1.1');
  // Botón generar
  await page.getByRole('button', { name: /Generar Informe Clínico/i }).click();
  await expect(page.getByText('Informe Clínico')).toBeVisible();
  await expect(page.getByText('Prompt Generado:')).toBeVisible();
});
