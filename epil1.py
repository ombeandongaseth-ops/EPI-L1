import os
from datetime import datetime
import pandas as pd
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Gestion des EPI - UCAC-ICAM", page_icon="🦺", layout="wide"
)

# Fichier de stockage des données
DB_FILE = "demandes_epi.csv"


# Fonction pour charger les données
def charger_donnees():
  if os.path.exists(DB_FILE):
    return pd.read_csv(DB_FILE, dtype=str)
  else:
    return pd.DataFrame(
        columns=[
            "Date",
            "Nom",
            "Prénom",
            "Téléphone",
            "Blouse",
            "Casque",
            "Gants isolants",
            "Gants de manutention",
            "Lunettes de protection",
            "Multimètre",
            "Chaussures de sécurité",
            "Pointure Chaussures",
        ]
    )


# Fonction pour sauvegarder les données
def sauvegarder_donnees(df):
  df.to_csv(DB_FILE, index=False)


# Liste des EPI standards
liste_epi_simples = [
    "Blouse",
    "Casque",
    "Gants isolants",
    "Gants de manutention",
    "Lunettes de protection",
    "Multimètre",
]

# --- MENU DE NAVIGATION ---
st.sidebar.title("Navigation 🦺")
menu = st.sidebar.radio(
    "Aller vers", ["Espace Étudiant (L1)", "Espace Administrateur"]
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
# 1. ESPACE ÉTUDIANT (L1)
# ==========================================
if menu == "Espace Étudiant (L1)":
  st.title("🦺 Demande d'EPI - Étudiants L1")
  st.markdown(
      "Remplis tes informations et coche les équipements qu'il te manque."
  )

  # Utilisation d'un st.form pour bloquer l'envoi si les champs obligatoires sont vides (évite les doublons)
  with st.form("form_epi_securise"):
    st.subheader("1. Vos Informations Personnelles")
    col1, col2 = st.columns(2)
    with col1:
      nom = st.text_input("Nom *").strip().upper()
    with col2:
      prenom = st.text_input("Prénom *").strip().capitalize()

    telephone = st.text_input("Numéro de téléphone *").strip()

    st.divider()
    st.subheader("2. Quels sont les EPI qu'il vous manque ?")

    # Cases à cocher pour les EPI standards
    choix_epi = {}
    for epi in liste_epi_simples:
      choix_epi[epi] = st.checkbox(epi)

    # Chaussures de sécurité et pointure (30 à 47)
    besoin_chaussures = st.checkbox("Chaussures de sécurité")
    pointure = st.selectbox(
        "👟 Précisez votre pointure de sécurité (si coché ci-dessus) :",
        options=[str(p) for p in range(30, 48)],
        index=11,  # Par défaut 41
    )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button(
        "Soumettre ma demande", type="primary", use_container_width=True
    )

    if submitted:
      if not nom or not prenom or not telephone:
        st.error(
            "⚠️ Veuillez impérativement remplir votre Nom, Prénom et Numéro de"
            " téléphone avant de soumettre."
        )
      else:
        df = charger_donnees()

        # Vérification anti-doublon (si l'étudiant avec le même nom/prénom/téléphone existe déjà)
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
          # Enregistrement de la nouvelle demande
          nouvelle_demande = {
              "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "Nom": nom,
              "Prénom": prenom,
              "Téléphone": telephone,
          }

          for epi in liste_epi_simples:
            nouvelle_demande[epi] = "Oui" if choix_epi[epi] else "Non"

          nouvelle_demande["Chaussures de sécurité"] = (
              "Oui" if besoin_chaussures else "Non"
          )
          nouvelle_demande["Pointure Chaussures"] = (
              str(pointure) if besoin_chaussures else "N/A"
          )

          df = pd.concat(
              [df, pd.DataFrame([nouvelle_demande])], ignore_index=True
          )
          sauvegarder_donnees(df)

          st.success(
              f"✅ Merci {prenom} ! Tes besoins en EPI ont bien été transmis à"
              " l'administration en toute sécurité."
          )

# ==========================================
# 2. ESPACE ADMINISTRATEUR
# ==========================================
elif menu == "Espace Administrateur":
  st.title("🔐 Espace Administrateur - Gestion & Recensement")

  mot_de_passe = st.sidebar.text_input("Mot de passe admin", type="password")
  ADMIN_PASSWORD = "icam"  # Mot de passe par défaut

  if mot_de_passe != ADMIN_PASSWORD:
    st.warning(
        "⚠️ Entrez le mot de passe administrateur pour consulter les demandes."
    )
  else:
    st.success("🔓 Accès autorisé.")
    df = charger_donnees()

    if df.empty:
      st.info("Aucune demande enregistrée pour le moment.")
    else:
      # Compteur total d'étudiants enregistrés
      st.info(
          f"📊 Nombre total d'étudiants ayant soumis leur demande :"
          f" **{len(df)}**"
      )

      # ==========================================
      # SECTION A : RECENSEMENT GLOBAL À ACHETER
      # ==========================================
      st.header("📊 1. Recensement global des achats à effectuer")
      st.markdown(
          "Voici la quantité totale d'équipements à commander pour toute la"
          " promo :"
      )

      # Calcul des totaux
      tous_les_epi = liste_epi_simples + ["Chaussures de sécurité"]
      totaux = {epi: (df[epi] == "Oui").sum() for epi in tous_les_epi}

      # Affichage sous forme de métriques
      cols = st.columns(3)
      for idx, (epi, total) in enumerate(totaux.items()):
        with cols[idx % 3]:
          st.metric(label=f"Totaux {epi}", value=int(total))

      # Détail des pointures de chaussures
      if totaux["Chaussures de sécurité"] > 0:
        st.subheader("👟 Détail des pointures de chaussures à commander")
        df_chaussures = df[df["Chaussures de sécurité"] == "Oui"]
        decompte_pointures = (
            df_chaussures["Pointure Chaussures"]
            .value_counts()
            .reset_index()
        )
        decompte_pointures.columns = ["Pointure", "Quantité à acheter"]
        st.table(decompte_pointures)

      st.divider()

      # ==========================================
      # SECTION B : DÉTAIL PAR ÉTUDIANT (QUI A BESOIN DE QUOI)
      # ==========================================
      st.header("📋 2. Détail nominatif (Qui a besoin de quoi ?)")
      st.markdown(
          "Consultez les besoins individuels et les coordonnées de chaque"
          " étudiant :"
      )


      def construire_resume_besoins(row):
        manquants = []
        for epi in liste_epi_simples:
          if row[epi] == "Oui":
            manquants.append(epi)
        if row["Chaussures de sécurité"] == "Oui":
          manquants.append(
              f"Chaussures de sécurité (Pointure {row['Pointure Chaussures']})"
          )

        if len(manquants) == 0:
          return "Aucun manque"
        return ", ".join(manquants)


      df_affichage = df[["Nom", "Prénom", "Téléphone", "Date"]].copy()
      df_affichage["Équipements manquants"] = df.apply(
          construire_resume_besoins, axis=1
      )

      st.dataframe(df_affichage, use_container_width=True)

      # Option de téléchargement du tableau complet
      csv = df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="📥 Télécharger la base de données complète (CSV)",
          data=csv,
          file_name=f"recensement_epi_l1_{datetime.now().strftime('%Y-%m-%d')}.csv",
          mime="text/csv",
      )

      # Option de nettoyage
      with st.expander("⚙️ Zone dangereuse"):
        if st.button("🗑️ Effacer toutes les données"):
          if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
