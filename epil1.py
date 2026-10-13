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
            "Promotion",
            "Résidence",
            "Lunettes (1er choix)",
            "Lunettes (2eme choix)",
            "Gants d'électricité (1er choix)",
            "Gants d'électricité (2eme choix)",
            "Gants de manutention",
            "Casque (1er choix)",
            "Casque (2eme choix)",
            "Chaussures - BEO WORK",
            "Chaussures - AMSTRON",
            "Chaussures - WALKMANDER",
            "Chaussures - Delta plus",
            "Pointure Chaussures",
            "Multimètre",
            "Blouse TP chimie",
        ]
    )


# Fonction pour sauvegarder les données
def sauvegarder_donnees(df):
  df.to_csv(DB_FILE, index=False)


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

    # Utilisation de index=None pour qu'aucun choix ne soit sélectionné par défaut
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

        # Vérification anti-doublon
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
          nouvelle_demande = {
              "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "Nom": nom,
              "Prénom": prenom,
              "Téléphone": telephone,
              "Promotion": promotion,
              "Résidence": residence,
              "Pointure Chaussures": pointure,
          }

          for article, choix in choix_articles.items():
            # Si l'étudiant n'a rien coché sur une ligne, on met "Non spécifié" par défaut
            nouvelle_demande[article] = choix if choix is not None else "Aucun"

          df = pd.concat(
              [df, pd.DataFrame([nouvelle_demande])], ignore_index=True
          )
          sauvegarder_donnees(df)

          st.success(
              f"✅ Merci {prenom} ! Tes informations ont bien été transmises à"
              " l'administration."
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
      st.info(
          f"📊 Nombre total d'étudiants ayant soumis leur fiche :"
          f" **{len(df)}**"
      )

      # Tri automatique par ordre alphabétique
      df = df.sort_values(by=["Nom", "Prénom"], ascending=[True, True])

      # ==========================================
      # SECTION A : RECENSEMENT GLOBAL DES ACHATS
      # ==========================================
      st.header("📊 1. Recensement global des achats et des coûts")
      st.markdown(
          "Voici les quantités totales à commander pour chaque équipement"
          " demandé ('Je veux') :"
      )

      prix_unitaires = {
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

      recensement_data = []
      for article, prix in prix_unitaires.items():
        if article in df.columns:
          quantite = (df[article] == "Je veux").sum()
          total_fcfa = quantite * prix
          recensement_data.append({
              "Équipement": article,
              "Prix unitaire": f"{prix:,} F",
              "Quantité à commander": int(quantite),
              "Coût Total": f"{total_fcfa:,} F",
          })

      df_recensement = pd.DataFrame(recensement_data)
      st.dataframe(df_recensement, use_container_width=True)

      # Détail des pointures de chaussures demandées
      st.subheader("👟 Répartition des pointures de chaussures demandées")
      chaussures_cols = [
          "Chaussures - BEO WORK",
          "Chaussures - AMSTRON",
          "Chaussures - WALKMANDER",
          "Chaussures - Delta plus",
      ]
      df_chaussures_voulues = df[
          (df[chaussures_cols] == "Je veux").any(axis=1)
      ]
      if not df_chaussures_voulues.empty:
        decompte_pointures = (
            df_chaussures_voulues["Pointure Chaussures"]
            .value_counts()
            .reset_index()
        )
        decompte_pointures.columns = ["Pointure", "Quantité"]
        st.table(decompte_pointures)
      else:
        st.info("Aucune demande de chaussures pour le moment.")

      st.divider()

      # ==========================================
      # SECTION B : DÉTAIL PAR ÉTUDIANT
      # ==========================================
      st.header(
          "📋 2. Détail nominatif (Trié par ordre alphabétique)"
      )
      st.markdown(
          "Consultez les choix individuels, la promotion et les coordonnées de"
          " chaque étudiant :"
      )


      def construire_resume_besoins(row):
        manquants = []
        for article in prix_unitaires.keys():
          if row[article] == "Je veux":
            if "Chaussures" in article:
              manquants.append(f"{article} (Pointure {row['Pointure Chaussures']})")
            else:
              manquants.append(article)
        if not manquants:
          return "Rien à commander"
        return ", ".join(manquants)


      df_affichage = df[
          ["Nom", "Prénom", "Téléphone", "Promotion", "Résidence", "Date"]
      ].copy()
      df_affichage["Équipements demandés"] = df.apply(
          construire_resume_besoins, axis=1
      )

      st.dataframe(df_affichage, use_container_width=True)

      # Option de téléchargement
      csv = df.to_csv(index=False).encode("utf-8")
      st.download_button(
          label="📥 Télécharger la base de données complète (CSV)",
          data=csv,
          file_name=f"recensement_epi_officiel_{datetime.now().strftime('%Y-%m-%d')}.csv",
          mime="text/csv",
      )

      # Option de nettoyage
      with st.expander("⚙️ Zone dangereuse"):
        if st.button("🗑️ Effacer toutes les données"):
          if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
