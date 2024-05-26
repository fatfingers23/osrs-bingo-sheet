/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_GSHEET_PASS_CODE_URL: string
    readonly VITE_GSHEET_BINGO_ITEMS_URL: string
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}
