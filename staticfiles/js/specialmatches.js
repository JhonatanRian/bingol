var sm = new Vue({
  el: '#bingoMatches',
  data() {
    return {
      hasPurchased: false,
      account: {
        authenticated: false,
        isSeller: false,
        nome: null,
        telefone: null
      },
      acumulado: 0,
      scheduled: [
        {
          matchId: null,
          premium: null,
          startedAt: null,
          ticketPrice: null,
          currentTickets: null,
          ticketsPerPlayer: null,
          show: false
        }
      ],
      sequence: {
        matchId: null,
        premium: null,
        startedAt: null,
        ticketPrice: null,
        currentTickets: null,
        ticketsPerPlayer: null,
        show: false
      },
      purchase: {
        quantity: 0,
        totalValue: 0,
        matchId: null,
        transactionId: null,
        dateConfirm: null,
        errorMessage: null
      },
      purchaseSequencial: {
        quantity: 0,
        totalValue: 0,
        matchId: null,
        transactionId: null,
        dateConfirm: null,
        errorMessage: null
      },
      noMatch: true
    };
  },

  methods: {
    run() {
      this.fillData();
    },

    fillData: function () {
      axios.get(baseUrl + '/api/special-matches')
        .then(response => {
          this.account = response.data.account;
          this.acumulado = response.data.acumulado;
          this.scheduled = response.data.scheduled;
          this.sequence = response.data.sequence;

          if (response.data.scheduled.length > 0) {
            this.noMatch = false;
          }

        })
        .catch(error => {
          console.log(error);
        });
    },

    collapse(match) {
      this.scheduled.forEach(function (m) {
        m.show = false;
      });
      this.purchase.quantity = 0;
      match.show = !(match.show)
    },

    increaseQuantity(match) {
      let limitPurchase = match.ticketsPerPlayer - match.currentTickets;
      if (this.account.isSeller) {
        limitPurchase = 1000;
      }
      if (this.purchase.quantity < limitPurchase) {
        this.purchase.quantity = parseInt(this.purchase.quantity) + 1;
      }
    },

    increaseQuantitySequencial(match) {
      let limitPurchase = match.ticketsPerPlayer - match.currentTickets;
      if (this.account.isSeller) {
        limitPurchase = 1000;
      }
      if (this.purchaseSequencial.quantity < limitPurchase) {
        this.purchaseSequencial.quantity = parseInt(this.purchaseSequencial.quantity) + 1;
      }
    },

    updateQuantity(el) {
      this.purchase.quantity = el.currentTarget.value;
    },

    updateQuantitySequencial(el) {
      this.purchaseSequencial.quantity = el.currentTarget.value;
    },

    confirmPurchase(match) {
      this.purchase.matchId = match.matchId;
      this.purchase.totalValue = this.purchase.quantity * match.ticketPrice;
    },

    confirmPurchaseSequencial(match) {
      this.purchaseSequencial.matchId = match.matchId;
      this.purchaseSequencial.totalValue = this.purchaseSequencial.quantity * match.ticketPrice;
    },

    reservar() {

      if (!this.hasPurchased) {
        this.hasPurchased = true;

        let params = new URLSearchParams();
        params.append('id', this.purchase.matchId);
        params.append('quantity', this.purchase.quantity);
        if (this.account.nome != null) {
          params.append('nome', this.account.nome)
        }
        if (this.account.telefone != null) {
          params.append('telefone', this.account.telefone)
        }

        axios.post(baseUrl + '/api/match/purchase-ticket/', params, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
          .then(response => {
            this.hasPurchased = false;

            if (response.data.ok != undefined) {
              this.purchase.dateConfirm = response.data.ok.date;
              this.purchase.transactionId = response.data.ok.transaction_id;

              $('#modalRodadasEspeciais').modal('hide');
              $('#modalRodadasEspeciaisFim').modal('show');

              let that = this;
              this.scheduled.forEach(function (match) {

                if (match.matchId == that.purchase.matchId) {
                  match.currentTickets = match.currentTickets + that.purchase.quantity;
                }
              });

            } else {
              this.purchase.errorMessage = response.data.error.message;
              $('#modalRodadasEspeciais').modal('hide');
              $('#modalRodadasEspeciaisError').modal('show');
            }
          });


      }


    },

    reservarSequencial() {

      if (!this.hasPurchased) {
        this.hasPurchased = true;

        let params = new URLSearchParams();
        params.append('id', this.purchaseSequencial.matchId);
        params.append('quantity', this.purchaseSequencial.quantity);
        if (this.account.nome != null) {
          params.append('nome', this.account.nome)
        }
        if (this.account.telefone != null) {
          params.append('telefone', this.account.telefone)
        }

        axios.post(baseUrl + '/api/match/purchase-ticket/', params, {headers: {'Content-Type': 'application/x-www-form-urlencoded'}})
          .then(response => {
            this.hasPurchased = false;

            if (response.data.ok != undefined) {
              this.purchaseSequencial.dateConfirm = response.data.ok.date;
              this.purchaseSequencial.transactionId = response.data.ok.transaction_id;

              $('#modalRodadasSequenciais').modal('hide');
              $('#modalRodadasSequenciaisFim').modal('show');

              let that = this;
              this.scheduled.forEach(function (match) {

                if (match.matchId == that.purchaseSequencial.matchId) {
                  match.currentTickets = match.currentTickets + that.purchaseSequencial.quantity;
                }
              });

            } else {
              this.purchaseSequencial.errorMessage = response.data.error.message;
              $('#modalRodadasSequenciais').modal('hide');
              $('#modalRodadasSequenciaisError').modal('show');
            }
          });


      }


    }

  },

  filters: {
    filterId: function (value) {
      if (value != null) {
        return String(value).padStart(10, '0');
      } else {
        return '';
      }
    },

    date: function (value) {
      if (value != null) {
        if (isSafari) {
          value = value.replace(/-/g, '/');
        }

        var date = new Date(Date.parse(String(value)));
        return date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear();
      } else {
        return '';
      }
    },

    hour: function (value) {
      if (value != null) {
        if (isSafari) {
          value = value.replace(/-/g, '/');
        }
        var date = new Date(Date.parse(String(value)));
        return date.getHours() + ':' + String(date.getMinutes()).padStart(2, '0') + 'h';
      } else {
        return '';
      }
    },

    filterCurrency: function (value) {
      if (value != null) {
        return parseFloat(value).toLocaleString('pt-BR', {minimumFractionDigits: 2});
      } else {
        return ''
      }
    },
  },

  created() {
    this.run();
    setTimeout(function () {
      $('#bingoMatches').removeClass('hide-vue')
    }, 3000);
  }
});
