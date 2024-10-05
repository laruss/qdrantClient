import type { ConfigFile } from '@rtk-query/codegen-openapi';

const config: ConfigFile = {
    schemaFile: 'http://localhost:8000/openapi.json',
    apiFile: './src/app/api/emptyApi.ts',
    apiImport: 'emptySplitApi',
    outputFile: './src/app/api/generatedApi.ts',
    exportName: 'generatedApi',
    hooks: false,
};

export default config;
