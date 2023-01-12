(($) => {
  const CopyLinkClick = {
    cacheDom() {
      this.buttonCall = $('.js-copy-link-click');
      this.modal = $("#modalLinkCadastro");
    },

    bindEvents() {
      this.buttonCall.on('click', this.action);
      this.modal.on('hidden.bs.modal', this.closeModal)
    },

    closeModal(el) {
      $('.status-copy').html('');
    },

    action(el) {
      el.preventDefault();
      const that = $(el.currentTarget);
      const target = that.data('target');
      const input = document.getElementById(target);
      input.focus();
      input.select();
      document.execCommand('copy');
      $('.status-copy').addClass('text-success').html('Link copiado!');
    },

    init() {
      this.cacheDom();
      this.bindEvents();
    },
  }.init();
})(jQuery);
