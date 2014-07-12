module ApplicationHelper

  # Retorna data no formato dd/mm/yyyy
  def formatarData data
    data[8..9]+'/'+data[5..6]+'/'+data[0..3]
  end

  # Substitui ((NG))texto((CL)) por <b>texto</b>
  def tagNegrito s
    s=s.gsub(/(\(\(NG\)\)((?!\(\(NG\)\)).)*\(\(CL\)\))/){|m|m.gsub(/\(\(NG\)\)/,'<b>').gsub(/\(\(CL\)\)/,'</b>')}
    s
  end

  # Retorna texto com formatacao HTML
  def textoFormatado s
    tagNegrito(s.gsub(/\n/, '<br />')).html_safe
  end

  # Retorna texto sem formatacao HTML
  def textoNaoFormatado(s, tags=nil)
    # Primeiro coloca as tags HTML depois as tira.
    # Tira todas tags exceto as contidas em 'tags' - Por exemplo <em> para o Highlight das palavras buscadas.
    ActionController::Base.helpers.sanitize(textoFormatado(s).gsub(/(\<br \/\>)/,'<br /> '), :tags=>tags)
  end

end
