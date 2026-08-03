# Bundled figure-example provenance

## Adopted chart atlas and synthetic gallery

The 15 PNG files in `chart-atlas/` and `gallery/` are copied byte-for-byte from
the adopted upstream snapshot:

- repository: <https://github.com/Yuan1z0825/nature-skills>
- revision: `fac88c419fa0ad642014609e3084f52629cfee52`
- upstream paths: `skills/nature-figure/assets/chart-atlas/` and
  `skills/nature-figure/assets/gallery/`

They are visual or structural examples, not experimental observations or
source data.

## Faithful paper gallery

`paper-patterns/` contains the complete curated output set from
<https://github.com/ChenLiu-1996/figures4papers> at revision
`6e9ca1200f4b1445cff68a42be76f7712ec2d4e1`:

- `python/`: 29 original Python-rendered PNGs and three companion PDFs from
  eight project families;
- `hybrid/`: ten original paper composites that were only partly made in
  Python;
- `optimized/`: three user-approved derived outputs (deterministic Cflows,
  deduplicated VIGIL ablation, and repaired Ophthal timeline), kept separate
  from the upstream golden files;
- `manifest.json`: source paths, registered scripts, dimensions, DPI metadata,
  SHA-256 hashes, and provenance.

The associated 25 Python files are organized under `../scripts/paper_examples/`.
All 42 upstream outputs remain byte-for-byte copies. Selected source files are
now narrowly curated; each such manifest record keeps both the current hash and
the upstream hash. Verify upstream outputs, current sources, and approved
optimized variants with:

```bash
python3 "$SKILL_DIR/scripts/check_paper_gallery.py"
```

Treat these outputs as immutable visual golden references. Do not regenerate
them through an unrelated analytical template, silently accept a changed render, or delete
a sample because its code or scientific convention needs review. Put proposed
repairs in a separate output path and compare them first.

## SHA-256 inventory for adopted atlas/gallery

```text
4a0e3040bbdbfe5ec48b66515f719f83ad7304fadb2e56432cd3e8f7ccbabd65  chart-atlas/atlas-01-bar-charts.png
9a8189149180a68679738bc4be152ee40b17d71261d71b3759d315a7169da0d9  chart-atlas/atlas-02-line-trends.png
40dd7c7c14c45b45cc22ee23e19f2dc1901f38b26a1fb4b0f26a30dbd10c0423  chart-atlas/atlas-03-heatmaps.png
1bbfbc38a3f246e4fd7c59b9ed1003ddbc7280ee160b7c38abf8d410b27fe6f8  chart-atlas/atlas-04-scatter-bubble.png
e7fa7d98cd4f5263f5550d7ac8824e60071c20b2927aef52ac6d18d62fd29ffa  chart-atlas/atlas-05-radar-polar.png
a1fe533d07dae36d11c997577ded61adb16bf5d4dd5c0dee2ff92ae570f0f01e  chart-atlas/atlas-06-distributions.png
dc61a5257eae4748348c72c51f2e70e59979c6892f52dadf7bb4ba6f8b98b00b  chart-atlas/atlas-07-forest-interval.png
350c25e427d945dee5fd98316eb6ebe307304b9d187d954a88c05852d664a60b  chart-atlas/atlas-08-area-stacked.png
bbc8c0b8708d42465e57cb7c56b4d2ecfbaa63340a5a6dfefbcb51189cd1a995  chart-atlas/atlas-09-image-plates.png
cd384abe10aa86bd310c1288a42f33735cb555c267bddae1ecd262905a7a1de5  chart-atlas/atlas-10-network-matrix.png
2e0706fae3256e1de2388f8605f35b9b6ac23cfc397161a952f34cc5fa2f2192  gallery/fig1-material-mechanism-rich.png
90081b3f778b9ede2dba41c60b6abf0c28a239060c69428344539529cd7f3257  gallery/fig2-spatial-imaging-rich.png
25d6fc50f5808104a7cb19f4795cea4229fbc6159fa7509f716a94f7c160a033  gallery/fig3-in-vivo-efficacy-rich.png
999edb06b942f988a51b11f947845e42e4c346b2f9e5d5a6425def9e43bb69d1  gallery/fig4-single-cell-systems-rich.png
245ad31f97b2054628987444e44d6a007f352f65ae6254189f5ed8ba9b0301c6  gallery/fig5-validation-perturbation-rich.png
```
