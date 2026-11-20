# Skema e metadata-ve v1 (Java 2)

Ndryshime kundrejt v0: origjina dhe autorizimi i fotove ruhen veçmas (`image_sources`), shtohet `data_origin` (dallon demo nga vëzhgimet reale), `date_time` është e detyrueshme dhe fushat kanë vlera të lejuara me kontroll (CHECK) në databazë. Tabelat `predictions` dhe `reviews` nga v0 shtyhen për javën 8–9, kur ka model dhe panel.

**Marrëdhënia:** një burim (`image_sources`) mund të ketë shumë vëzhgime (`observations`). Çelësi i huaj: `observations.source_id -> image_sources.source_id`.

## Tabela `observations`

| Fusha | Përshkrimi | Tipi | Statusi | Vlera të lejuara / shënime |
|---|---|---|---|---|
| `observation_id` | ID unike e vëzhgimit (çelës primar) | TEXT | E detyrueshme | p.sh. `DEMO-001` |
| `image_path` | Rruga e fotos në projekt | TEXT | E detyrueshme | Fotot nuk ruhen në Git |
| `image_hash` | SHA-256 i fotos, për deduplikim | TEXT | Opsionale | Mund të mungojë për demo |
| `class_label` | Grupi vizual i insektit | TEXT | Opsionale | Provizore deri në Javën 4; mund të mbetet bosh |
| `label_status` | Statusi i etiketës | TEXT | E detyrueshme | `demo`, `unverified`, `community_verified`, `expert_confirmed`, `rejected` |
| `expert_review` | Verifikimi nga eksperti | TEXT | E detyrueshme (parazgjedhje `pending`) | `pending`, `approved`, `rejected`, `not_applicable` |
| `data_origin` | Origjina e vëzhgimit | TEXT | E detyrueshme | `demo`, `public_platform`, `own_photo` |
| `group_id` | Sesion/ditë/individ për ndarje pa leakage | TEXT | Opsionale (e rekomanduar) | Foto të të njëjtit grup ndahen së bashku |
| `plot_id` | Parcela, e pseudonimizuar | TEXT | Opsionale | p.sh. `P01`; pa emra ose koordinata të sakta |
| `date_time` | Data (dhe ora) e vëzhgimit | TEXT | E detyrueshme | `YYYY-MM-DD` ose `YYYY-MM-DD HH:MM` |
| `crop_type` | Kultura | TEXT | Opsionale | p.sh. `tomato` |
| `phenophase` | Faza e bimës | TEXT | Opsionale | Vetëm kur dihet |
| `device` | Pajisja e fotografimit | TEXT | Opsionale | |
| `observation_method` | Mënyra e fotografimit | TEXT | Opsionale | p.sh. `close-up`, `crop` |
| `source_id` | Lidhja me burimin | INTEGER | E detyrueshme | Çelës i huaj te `image_sources` |
| `created_at` | Koha e regjistrimit në databazë | TEXT | Automatike | |

## Tabela `image_sources`

| Fusha | Përshkrimi | Tipi | Statusi | Vlera të lejuara / shënime |
|---|---|---|---|---|
| `source_id` | ID e burimit (çelës primar, automatik) | INTEGER | Automatike | |
| `source_name` | Emri i burimit | TEXT | E detyrueshme | p.sh. `iNaturalist`, `Foto e ekipit`, `DEMO` |
| `source_url` | Adresa e fotos/vëzhgimit | TEXT | Opsionale | Foto lokale nuk kanë URL |
| `author` | Autori | TEXT | Opsionale | E detyrueshme për foto reale (atribuim) |
| `license` | Licenca ose leja | TEXT | E detyrueshme | p.sh. `CC0`, `CC-BY`, `own`, `DEMO` |
| `consent_status` | Statusi i autorizimit | TEXT | E detyrueshme | `own`, `cc_open`, `permission_granted`, `demo`, `unverified` |
| `notes` | Shënime | TEXT | Opsionale | |

## Rregulla

- Rreshtat me `data_origin = demo` janë të dhëna demonstrimi, **jo vëzhgime reale**. Nuk përdoren për rezultate shkencore.
- Për foto reale (`public_platform`), `author`, `source_url` dhe `license` duhet të plotësohen dhe të verifikohen (Java 3).
- Fusha që mund të mbeten bosh ruhen si NULL.
- Identiteti ose vendndodhja e saktë e fermerëve nuk ruhet pa leje.
