import os
from datetime import datetime
import pandas as pd
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Gestion des EPI - UCAC-ICAM", page_icon="🦺", layout="wide"
)

# Fichier de stockage des données
DB_FILE = "demandes_epi_officiel.csv"

# Dictionnaire des prix unitaires officiels
PRIX_UNITAIRES = {
    "Lunettes (1er choix)": 1500,
    "Lunettes (2eme choix)": 1500,
    "Gants d'électricité (1er choix)": 1500,
    "Gants d'électricité (2eme choix)": 1500,
    "Gants de manutention": 2000,
    "Casque (1er choix)": 5000,
    "Casque (2eme choix)": 3000,
    "Chaussures - BEO WORK": 12000,
    "Chaussures - AMSTRON": 12000,
    "Chaussures - WALKMANDER": 10000,
    "Chaussures - Delta plus": 15000,
    "Multimètre": 20000,
    "Blouse TP chimie": 4000,
}


# Fonction pour charger les données
def charger_donnees():
  if os.path.exists(DB_FILE):
    # Lecture avec utf-8-sig pour bien gérer les accents
    df = pd.read_csv(DB_FILE, dtype=str, encoding="utf-8-sig")
    if "Statut Paiement" not in df.columns:
      df["Statut Paiement"] = "Impayé"
    return df
  else:
    colonnes = [
        "Date",
        "Nom",
        "Prénom",
        "Téléphone",
        "Promotion",
        "Résidence",
        "Pointure Chaussures",
        "Statut Paiement",
    ] + list(PRIX_UNITAIRES.keys())
    return pd.DataFrame(columns=colonnes)


# Fonction pour sauvegarder les données (corrigée avec utf-8-sig pour Excel)
def sauvegarder_donnees(df):
  df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")


# --- MENU DE NAVIGATION ---
st.sidebar.title("Navigation 🦺")
menu = st.sidebar.radio(
    "Aller vers", ["Espace Étudiant (L1 / BP)", "Espace Administrateur"]
)

# ==========================================
# REMERCIEMENTS (EN HAUT DE PAGE)
# ==========================================
st.markdown(
    "💡 **Projet collaboratif** — Remerciements particuliers à"
    " **Gedidia-chérubin L2-2030** pour sa contribution à la création de cette"
    " application 🦺"
)
st.divider()

# ==========================================
# 1. ESPACE ÉTUDIANT
# ==========================================
if menu == "Espace Étudiant (L1 / BP)":
  st.title("🦺 Fiche de Recensement des EPI - UCAC-ICAM")
  st.markdown(
      "Remplis tes informations personnelles et indique les équipements dont"
      " tu as besoin."
  )

  with st.form("form_epi_officiel"):
    st.subheader("1. Informations Personnelles")
    col1, col2 = st.columns(2)
    with col1:
      nom = st.text_input("Nom *").strip().upper()
      promotion = st.radio("Promotion *", ["L1", "BP"], horizontal=True)
    with col2:
      prenom = st.text_input("Prénom *").strip().capitalize()
      residence = st.radio(
          "Résident(e) *", ["Interne", "Externe"], horizontal=True
      )

    telephone = st.text_input("Numéro de téléphone *").strip()

    st.divider()
    st.subheader("2. Choix des Équipements")
    st.markdown(
        "_Veuillez préciser pour chaque article si vous le voulez ou si vous"
        " l'avez déjà._"
    )

    choix_articles = {}

    st.markdown("### 👓 Lunettes de protection (1 500 F)")
    choix_articles["Lunettes (1er choix)"] = st.radio(
        "Lunettes de protection 1er choix (1500F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )
    choix_articles["Lunettes (2eme choix)"] = st.radio(
        "Lunettes de protection 2eme choix (1500F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )

    st.markdown("### ⚡ Gants d'électricité (1 500 F)")
    choix_articles["Gants d'électricité (1er choix)"] = st.radio(
        "Gants d'électricité 1er choix (1500F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )
    choix_articles["Gants d'électricité (2eme choix)"] = st.radio(
        "Gants d'électricité 2eme choix (1500F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )

    st.markdown("### 🛠️ Gants de manutention (2 000 F)")
    choix_articles["Gants de manutention"] = st.radio(
        "Gants de manutention (2000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )

    st.markdown("### ⛑️ Casque de sécurité")
    choix_articles["Casque (1er choix)"] = st.radio(
        "Casque de sécurité 1er choix (5000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )
    choix_articles["Casque (2eme choix)"] = st.radio(
        "Casque de sécurité 2eme choix (3000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )

    st.markdown("### 👞 Chaussures de protection")
    choix_articles["Chaussures - BEO WORK"] = st.radio(
        "BEO WORK (12000F)", ["Je veux", "J'ai déjà"], horizontal=True, index=None
    )
    choix_articles["Chaussures - AMSTRON"] = st.radio(
        "AMSTRON (12000F)", ["Je veux", "J'ai déjà"], horizontal=True, index=None
    )
    choix_articles["Chaussures - WALKMANDER"] = st.radio(
        "WALKMANDER (10000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )
    choix_articles["Chaussures - Delta plus"] = st.radio(
        "Delta plus (15000F)", ["Je veux", "J'ai déjà"], horizontal=True, index=None
    )

    pointure = st.selectbox(
        "👟 Précisez votre pointure de chaussures (30 à 47) :",
        options=[str(p) for p in range(30, 48)],
        index=11,  # Par défaut 41
    )

    st.markdown("### 🔌 Multimètre & Blouse")
    choix_articles["Multimètre"] = st.radio(
        "MULTIMETRE (20000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )
    choix_articles["Blouse TP chimie"] = st.radio(
        "Blouse de TP chimie (4000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button(
        "Soumettre ma demande", type="primary", use_container_width=True
    )

    if submitted:
      if not nom or not prenom or not telephone:
        st.error(
            "⚠️ Veuillez impérativement remplir votre Nom, Prénom et Numéro de"
            " téléphone."
        )
      else:
        df = charger_donnees()

        doublon = False
        if not df.empty:
          doublon = (
              (df["Nom"] == nom)
              & (df["Prénom"] == prenom)
              & (df["Téléphone"] == telephone)
          ).any()

        if doublon:
          st.warning(
              f"⚠️ {prenom} {nom}, une demande a déjà été enregistrée avec"
              " ces informations !"
          )
        else:
          montant_total = 0
          articles_demandes = []
          for article, choix in choix_articles.items():
            statut = choix if choix is not None else "Aucun"
            if statut == "Je veux":
              montant_total += PRIX_UNITAIRES[article]
              articles_demandes.append(article)

          nouvelle_demande = {
              "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "Nom": nom,
              "Prénom": prenom,
              "Téléphone": telephone,
              "Promotion": promotion,
              "Résidence": residence,
              "Pointure Chaussures": pointure,
              "Statut Paiement": "Impayé",
          }

          for article, choix in choix_articles.items():
            nouvelle_demande[article] = choix if choix is not None else "Aucun"

          df = pd.concat(
              [df, pd.DataFrame([nouvelle_demande])], ignore_index=True
          )
          sauvegarder_donnees(df)

          st.success(
              f"✅ Merci {prenom} ! Tes informations ont bien été transmises à"
              " l'administration."
          )

          st.markdown("---")
          st.subheader("💳 Récapitulatif de votre commande et Paiement")
          if montant_total > 0:
            st.info(
                f"💰 **Montant total à régler : {montant_total:,} FCFA**"
            )
            st.write(
                "**Équipements commandés :** " + ", ".join(articles_demandes)
            )

            st.markdown(
                "### 📲 Instructions pour le paiement :\n"
                "Veuillez contacter le **BDE (Bureau Des Étudiants)** pour"
                " effectuer le règlement de vos équipements :\n"
                "- **Destinataire :** Le BDE UCAC-ICAM\n"
                "- **Important :** N'oubliez pas de préciser votre **Nom,"
                f" Prénom et Promotion ({promotion})** lors du paiement."
            )
          else:
            st.success(
                "🎉 Vous avez indiqué posséder déjà tous les équipements !"
                " Aucun frais à payer."
            )

# ==========================================
# 2. ESPACE ADMINISTRATEUR
# ==========================================
elif menu == "Espace Administrateur":
  st.title("🔐 Espace Administrateur - Gestion & Recensement")

  mot_de_passe = st.sidebar.text_input("Mot de passe admin", type="password")
  ADMIN_PASSWORD = "icam"

  if "admin_connecte" not in st.session_state:
    st.session_state.admin_connecte = False

  if mot_de_passe == ADMIN_PASSWORD:
    st.session_state.admin_connecte = True

  if not st.session_state.admin_connecte:
    st.warning(
        "⚠️ Entrez le mot de passe administrateur pour consulter les demandes."
    )
  else:
    st.success("🔓 Accès autorisé.")
    df = charger_donnees()

    if df.empty:
      st.info("Aucune demande enregistrée pour le moment.")
    else:
      st.info(
          f"📊 Nombre total d'étudiants ayant soumis leur fiche :"
          f" **{len(df)}**"
      )

      df = df.sort_values(by=["Nom", "Prénom"], ascending=[True, True])
      df = df.reset_index(drop=True)

      # ==========================================
      # SECTION A : RECENSEMENT GLOBAL ET BUDGET TOTAL
      # ==========================================
      st.header("📊 1. Recensement global des achats et des coûts")

      recensement_data = []
      grand_total_general = 0

      for article, prix in PRIX_UNITAIRES.items():
        if article in df.columns:
          quantite = (df[article] == "Je veux").sum()
          total_fcfa = quantite * prix
          grand_total_general += total_fcfa
          recensement_data.append({
              "Équipement": article,
              "Prix unitaire": f"{prix:,} F",
              "Quantité à commander": int(quantite),
              "Coût Total": f"{total_fcfa:,} F",
          })

      st.metric(
          label="💰 COÛT TOTAL GÉNÉRAL DE TOUS LES ÉQUIPEMENTS À ACHETER",
          value=f"{grand_total_general:,} FCFA",
      )
      st.markdown("<br>", unsafe_allow_html=True)

      df_recensement = pd.DataFrame(recensement_data)
      st.dataframe(df_recensement, use_container_width=True)

      # ==========================================
      # SECTION CHAUSSURES : MARQUE + POINTURE + PRIX
      # ==========================================
      st.subheader(
          "👟 Détail des chaussures commandées (Marque, Pointure, Prix &"
          " Quantité)"
      )
      chaussures_cols = {
          "Chaussures - BEO WORK": 12000,
          "Chaussures - AMSTRON": 12000,
          "Chaussures - WALKMANDER": 10000,
          "Chaussures - Delta plus": 15000,
      }

      details_chaussures = []
      for col, prix_unit in chaussures_cols.items():
        df_marque = df[df[col] == "Je veux"]
        if not df_marque.empty:
          decompte = df_marque["Pointure Chaussures"].value_counts()
          for pointure, qté in decompte.items():
            cout_total_ligne = int(qté) * prix_unit
            details_chaussures.append({
                "Marque de Chaussure": col.replace("Chaussures - ", ""),
                "Pointure": pointure,
                "Prix unitaire": f"{prix_unit:,} F",
                "Quantité": int(qté),
                "Coût Total": f"{cout_total_ligne:,} F",
            })

      if details_chaussures:
        df_details_chaussures = pd.DataFrame(details_chaussures)
        df_details_chaussures = df_details_chaussures.sort_values(
            by=["Marque de Chaussure", "Pointure"]
        ).reset_index(drop=True)
        st.dataframe(df_details_chaussures, use_container_width=True)
      else:
        st.info("Aucune demande de chaussures pour le moment.")

      st.divider()

      # ==========================================
      # SECTION B : GESTION DES STATUTS DE PAIEMENT & DÉTAIL NOMINATIF
      # ==========================================
      st.header(
          "📋 2. Validation des Paiements & Détail Nominatif (Ordre"
          " alphabétique)"
      )
      st.markdown(
          "Vous pouvez modifier manuellement le statut de paiement d'un"
          " étudiant ci-dessous :"
      )


      def construire_resume_besoins(row):
        manquants = []
        for article in PRIX_UNITAIRES.keys():
          if row[article] == "Je veux":
            if "Chaussures" in article:
              manquants.append(f"{article} (Pt {row['Pointure Chaussures']})")
            else:
              manquants.append(article)
        if not manquants:
          return "Rien à commander"
        return ", ".join(manquants)


      df["Équipements demandés"] = df.apply(
          construire_resume_besoins, axis=1
      )

      colonnes_a_afficher = [
          "Nom",
          "Prénom",
          "Promotion",
          "Téléphone",
          "Statut Paiement",
          "Équipements demandés",
      ]

      df_edit = st.data_editor(
          df[colonnes_a_afficher],
          use_container_width=True,
          num_rows="fixed",
          key="editeur_paiement",
      )

      if not df_edit.equals(df[colonnes_a_afficher]):
        df["Statut Paiement"] = df_edit["Statut Paiement"]
        sauvegarder_donnees(df)
        st.success(
            "✅ Statut de paiement mis à jour avec succès dans la base de"
            " données !"
        )
        st.rerun()

      st.markdown("<br>", unsafe_allow_html=True)

      csv = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
      st.download_button(
          label="📥 Télécharger la base de données complète (CSV)",
          data=csv,
          file_name=f"recensement_epi_officiel_{datetime.now().strftime('%Y-%m-%d')}.csv",
          mime="text/csv",
      )

      with st.expander("⚙️ Zone dangereuse"):
        if st.button("🗑️ Effacer toutes les données"):
          if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
