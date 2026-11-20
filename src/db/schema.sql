-- Skema SQLite v1 (Java 2). Projekti 03: monitorimi i agrobiodiversitetit me AI.
-- Dy tabela: burimet/autorizimet ruhen veçmas nga vëzhgimet.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS image_sources (
    source_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name    TEXT NOT NULL,              -- p.sh. iNaturalist, Foto e ekipit, DEMO
    source_url     TEXT,                       -- opsionale (foto lokale nuk kanë URL)
    author         TEXT,                       -- opsionale per demo
    license        TEXT NOT NULL,              -- p.sh. CC0, CC-BY, own, DEMO
    consent_status TEXT NOT NULL
        CHECK (consent_status IN ('own','cc_open','permission_granted','demo','unverified')),
    notes          TEXT
);

CREATE TABLE IF NOT EXISTS observations (
    observation_id     TEXT PRIMARY KEY,
    image_path         TEXT NOT NULL,
    image_hash         TEXT,                   -- SHA-256; mund të mungojë për demo
    class_label        TEXT,                   -- mund të mbetet bosh (pa etiketë)
    label_status       TEXT NOT NULL
        CHECK (label_status IN ('demo','unverified','community_verified','expert_confirmed','rejected')),
    expert_review      TEXT NOT NULL DEFAULT 'pending'
        CHECK (expert_review IN ('pending','approved','rejected','not_applicable')),
    data_origin        TEXT NOT NULL
        CHECK (data_origin IN ('demo','public_platform','own_photo')),
    group_id           TEXT,                   -- sesion/ditë/individ, për ndarje pa leakage
    plot_id            TEXT,                   -- pseudonimizuar, p.sh. P01
    date_time          TEXT NOT NULL,          -- ISO: YYYY-MM-DD ose YYYY-MM-DD HH:MM
    crop_type          TEXT,
    phenophase         TEXT,
    device             TEXT,
    observation_method TEXT,
    source_id          INTEGER NOT NULL REFERENCES image_sources(source_id),
    created_at         TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_obs_date  ON observations(date_time);
CREATE INDEX IF NOT EXISTS idx_obs_plot  ON observations(plot_id);
CREATE INDEX IF NOT EXISTS idx_obs_class ON observations(class_label);
