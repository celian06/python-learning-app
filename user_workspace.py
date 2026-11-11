def calculer_prix_ttc(args):
    ht, tva = args
    return round(ht * (1 + tva), 2)