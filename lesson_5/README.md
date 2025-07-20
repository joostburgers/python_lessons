# Lesson 5: Geoparsing and Sentiment Mapping

## 🎯 Overview

This lesson teaches students how to extract geographic locations from text and visualize sentiment patterns on interactive maps. It combines advanced natural language processing, geospatial analysis, and data visualization.

## 📋 Lesson Structure (Streamlined)

### 1. **lesson_5_0_installation_setup.ipynb** ⚡
**Purpose**: One-stop installation and verification
- Installs all required packages automatically
- Downloads necessary AI models
- Verifies everything works correctly
- **Run this first!**

### 2. **lesson_5_geoparsing_mapping.ipynb** 📚
**Purpose**: Main lesson content
- **Part 1**: Initialize geoparser system
- **Part 2**: Load and process historical text data  
- **Part 3**: Work with complete geoparsed dataset
- **Part 4**: Create interactive sentiment maps

## 🔧 Installation Requirements

### System Requirements:
- **Python 3.8+**
- **2GB+ free disk space** (for AI models)
- **Internet connection** (for model downloads)
- **8GB+ RAM recommended**

### Key Dependencies:
- `geoparser`: Advanced geographic entity recognition
- `spacy + en_core_web_trf`: Language processing model
- `plotly`: Interactive visualization
- `mapclassify`: Data bucketing for maps
- `pandas, tqdm`: Data manipulation

## 🚀 Quick Start Guide

1. **Installation** (5-10 minutes):
   ```
   Open: lesson_5_0_installation_setup.ipynb
   Run all cells in order
   Wait for completion
   ```

2. **Main Lesson** (1-2 hours):
   ```
   Open: lesson_5_geoparsing_mapping.ipynb
   Follow the guided steps
   Experiment with the interactive maps
   ```

## 📁 Required Data Files

The lesson uses these data files from previous lessons:
- `df_virginia_toponym_sentiment_full.pickle` (sentiment analysis results)
- `df_virginia_geoparsed_complete.pickle` (pre-processed geoparsing results)
- `df_geolocations_sentiments.pickle` (aggregated location sentiment data)
- `df_geolocations_sentiments_small.pickle` (filtered dataset for mapping)

**Note**: Some files will be generated during the lesson if missing.

## 🎓 Learning Outcomes

Students will learn to:

### Technical Skills:
- Use advanced AI models for text processing
- Extract and resolve geographic references in text
- Combine multiple data sources (text + location + sentiment)
- Create interactive maps with custom styling
- Handle real-world data challenges (false positives, scale differences)

### Conceptual Understanding:
- How modern geoparsing works (transformer models + gazetteers)
- Geographic information systems (coordinates, administrative boundaries)
- Data visualization best practices for geospatial data
- The intersection of digital humanities and data science

## 🔍 What's New/Improved

### Previous Issues Fixed:
1. **Complex Installation**: Now one-click setup with verification
2. **Scattered Instructions**: Clear step-by-step progression
3. **Error-Prone Process**: Comprehensive error handling throughout
4. **Long Processing Times**: Pre-computed datasets + efficient functions
5. **Unclear Objectives**: Explicit learning goals for each section

### Enhancements Added:
- **Automated Dependency Management**: No manual pip installs
- **Progress Indicators**: Visual feedback during long operations
- **Error Recovery**: Helpful error messages with solutions
- **Interactive Elements**: Engaging visualizations and examples
- **Professional Output**: Publication-quality maps and analysis

## 🛠️ Troubleshooting

### Common Issues:

**1. Installation Fails**
- Check internet connection
- Verify sufficient disk space (2GB+)
- Try restarting kernel and re-running installation

**2. Geoparser Initialization Errors**
- Ensure installation notebook completed successfully
- Check that spaCy model downloaded correctly
- Restart kernel and try again

**3. Data Files Missing**
- Some files generated during lesson if missing
- Check file paths are correct
- Ensure you're in the lesson_5 directory

**4. Memory Issues**
- Close other applications
- Restart kernel to free memory
- Use the provided sample datasets instead of full datasets

### Getting Help:
1. Check error messages carefully - they include solutions
2. Review the installation verification section
3. Try restarting the kernel and re-running from the beginning
4. Ensure all prerequisites from previous lessons are met

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ Installation notebook completes without errors
- ✅ Geoparser successfully identifies locations in test sentences
- ✅ Interactive maps display correctly in your browser
- ✅ You can modify map parameters and see results change

## 📚 Extension Activities

For advanced students:
1. **Custom Data**: Apply the workflow to your own text corpus
2. **Temporal Analysis**: Add time dimensions to sentiment mapping
3. **Comparative Studies**: Compare sentiment across different authors/periods
4. **Integration**: Combine with demographic or economic data
5. **Publication**: Export maps for use in presentations or papers

---

## 📖 Pedagogical Notes

### Time Allocation:
- **Setup**: 10-15 minutes
- **Core Lesson**: 90-120 minutes  
- **Extensions**: 30-60 minutes

### Assessment Opportunities:
- **Technical**: Can students successfully run the complete pipeline?
- **Analytical**: Can students interpret the geographic sentiment patterns?
- **Creative**: Can students propose novel applications of the techniques?
- **Critical**: Can students identify limitations and potential biases in the approach?

### Cross-Curricular Connections:
- **Geography**: Spatial analysis and cartographic principles
- **History**: Historical text analysis and digital humanities methods
- **Computer Science**: AI/ML applications and data pipelines
- **Statistics**: Data aggregation and visualization techniques
