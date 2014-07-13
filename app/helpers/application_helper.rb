module ApplicationHelper

  # Retorna data no formato dd/mm/yyyy
  def formatarData data
    data[8..9]+'/'+data[5..6]+'/'+data[0..3]
  end

  # Substitui ((NG))texto((CL)) por <b>texto</b>
  def tagNegrito s
    s.gsub(/(\(\(NG\)\)((?!\(\(NG\)\)).)*\(\(CL\)\))/i){|m|m.gsub(/\(\(NG\)\)/i,'<b>').gsub(/\(\(CL\)\)/i,'</b>')}
  end

  # Substitui ((TITULO))titulo((TEXTO)) por <h4><b>titulo</b></h4>
  def tagTitulo s
    s.gsub(/(\(\(TITULO\)\)((?!\(\(TITULO\)\)).)*\(\(TEXTO\)\))/i){|m|m.gsub(/\(\(TITULO\)\)/i,'<h4><b>').gsub(/\(\(TEXTO\)\)/i,'</b></h4>')}
  end

  # Substitui ((tag)) por ''
  def retirarTags s
    s.gsub(/\(\(NG\)\)/i,'').gsub(/\(\(CL\)\)/i,'').gsub(/\(\(TITULO\)\)/i,'').gsub(/\(\(TEXTO\)\)/i,'')
  end

  # Retorna texto com formatacao HTML
  def textoFormatado s
    retirarTags(tagTitulo(tagNegrito(s.gsub(/\n/, '<br />')))).html_safe
  end

  # Retorna texto sem formatacao HTML
  def textoNaoFormatado(s, tags=nil)
    # Primeiro coloca as tags HTML depois as tira.
    # Tira todas tags exceto as contidas em 'tags' - Por exemplo <em> para o Highlight das palavras buscadas.
    ActionController::Base.helpers.sanitize(textoFormatado(s).gsub(/(\<br \/\>)/,'<br /> '), :tags=>tags)
  end

end
