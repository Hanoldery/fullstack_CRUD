module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'zimmer',
    meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { hid: 'description', name: 'description', content: 'Hans Zimmer Official Website' }
    ],
    link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ],
  },
  css: [
    '@/assets/main.scss',
    '@/assets/MaterialDesign/scss/materialdesignicons.scss'
  ],
  plugins: [
        '~plugins/import.js',
        '~plugins/filter.js'],
  modules: [
        '@nuxtjs/vuetify',
        '@nuxtjs/proxy',
        '@nuxtjs/axios'
  ],
  axios: {
        prefix: '/api/',
        proxy: true, // Can be also an object with default options
  },
  proxy: {
    '/api/': process.env.API_URL || 'http://0.0.0.0:4000',
/*    '/api/': process.env.API_URL || 'http://back:4000'*/
  },
  /*
  ** Customize the progress bar color
  */
  loading: { color: '#3B8070' },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** Run ESLint on save
    */
    extend (config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    }
  }
}
