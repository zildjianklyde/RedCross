module.exports = {
    content: [
      './app/templates/**/*.html',
      './node_modules/flowbite/**/*.js'
    ],
    theme: {
      extend: {
        colors: {
          'blood-red': '#cc0000',
          'donor-primary': '#0ea5e9'
        }
      },
    },
    plugins: [
      require('flowbite/plugin'),
      require('flowbite-typography')
    ]
  }