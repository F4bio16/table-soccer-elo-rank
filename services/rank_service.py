"""Modulo contentente il servizio RankService per le operazioni sui punteggi"""

class RankService:
    """RankService class"""
    def __init__(self, multiplicator_factor):
        self.multiplicator_factor = multiplicator_factor

    def calculate_expected_score(self, ranking1, ranking2):
        """
          Metodo per calcolare il punteggio atteso trà il giocatore con
          ranking1 e il giocatore con ranking2.
          Si applica la formula di Elo
        """
        return 1 / (1+ 10 ** ((ranking2 - ranking1) / 400)) # Elo formula

    def get_match_score(self, score, winner_score):
        """Calcola il punteggio del match

          valore tra 0 e 1 riferito al risultato della partita:
              .) 1 per partita vinta
              .) (punteggio_squadra / punteggio_massimo) * 0.6 -> per partita persa
        """
        print(f"get_match_score: passed score: {score} winner_score: {winner_score}")

        if score == winner_score:
            return 1

        return (score / winner_score) * 0.6

    def calculate_ranking_points(self, match_score, expected_score):
        """
          Metodo per calcolare i punti da aggiungere ad un singolo giocatore
          dopo la fine di una partita
        """

        return int((match_score - expected_score) * self.multiplicator_factor)
