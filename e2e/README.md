# E2E Tests (Playwright)

Placeholder specs creados:
- `upload_autofill.spec.ts`
- `medication_dedupe.spec.ts`

Pasos sugeridos:
1. Instalar deps Node (requiere Node 18+):
   npm install
   npx playwright install
2. Ajustar `baseURL` en `playwright.config.ts` si el front Reflex corre en otro puerto.
3. Reemplazar selectores placeholder (#file-labs, #med-input, #med-add, #med-list) por los reales.
4. Añadir asserts concretos (texto de reporte, conteo labs, etc.).
5. Integrar en CI (job separado usando `npx playwright test --reporter=line`).

Generar reporte HTML:
  npm run e2e && npm run e2e:report
