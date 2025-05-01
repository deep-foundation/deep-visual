export default {
  logo: (
    <span style={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
      <img src="/img/link_dark.png" alt="DeepVisual Logo" style={{ height: '24px', width: '24px' }} />
      DeepVisual
    </span>
  ),
  project: {
    link: 'https://github.com/deep-foundation/deep-visual'
  },
  docsRepositoryBase: 'https://github.com/deep-foundation/deep-visual/tree/main/doc',
  useNextSeoProps() {
    return {
      titleTemplate: '%s – DeepVisual'
    }
  },
  head: (
    <>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta name="description" content="DeepVisual: A Python library for advanced graph visualizations" />
      <meta name="og:title" content="DeepVisual Documentation" />
      <link rel="icon" href="/img/link_dark.png" />
      <link
        rel="icon"
        href="/img/link_not_white.png"
        media="(prefers-color-scheme: dark)"
      />
      <link
        rel="icon"
        href="/img/link_not_black.png"
        media="(prefers-color-scheme: light)"
      />
    </>
  ),
  footer: {
    text: `DeepVisual © ${new Date().getFullYear()}`
  },
  primaryHue: 210,
  primarySaturation: 100
} 