module ApplicationHelper

  # Retorna data no formato dd/mm/yyyy
  def formatarData data
    data[8..9]+'/'+data[5..6]+'/'+data[0..3]
  end

  def search_url_format(format)
    fullpath = request.fullpath
    if fullpath.include?("catalog") && !fullpath.include?(format)
      fullpath = fullpath.gsub("catalog","catalog."+format)
    else
      fullpath = fullpath.gsub("?","catalog."+format+"?")
    end
  end

  # Substitui ((NG))texto((CL)) por <b>texto</b>
  def tagNegrito s
    s.gsub(/(\(\(NG\)\)((?!\(\(NG\)\)).)*\(\(CL\)\))/i){|m|m.gsub(/\(\(NG\)\)/i,'<b>').gsub(/\(\(CL\)\)/i,'</b>')}
  end

  # Substitui ((TITULO))titulo((TEXTO)) por <h4><b>titulo</b></h4>
  def tagTitulo s
    s.gsub(/(\(\(TITULO\)\)((?!\(\(TITULO\)\)).)*\(\(TEXTO\)\))/i){|m|m.gsub(/\(\(TITULO\)\)/i,'<h4><b>').gsub(/\(\(TEXTO\)\)/i,'</b></h4>')}
    s.gsub(/(\(\(TÍTULO\)\)((?!\(\(TÍTULO\)\)).)*\(\(TEXTO\)\))/i){|m|m.gsub(/\(\(TÍTULO\)\)/i,'<h4><b>').gsub(/\(\(TEXTO\)\)/i,'</b></h4>')}
  end

  # Substitui ((tag)) por ''
  def retirarTags s
    s.gsub(/\(\(NG\)\)/i,'').gsub(/\(\(CL\)\)/i,'').gsub(/\(\(TITULO\)\)/i,'').gsub(/\(\(TÍTULO\)\)/i,'').gsub(/\(\(TEXTO\)\)/i,'')
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

  def botaoExportador(texto, link)
    ('<a class="btn btn-primary btn-sm" href="%s" role="button"><span class="glyphicon glyphicon glyphicon-download"></span> %s</a>' % [link, texto]).html_safe
  end

  def nomeEstilizado
    '<span class="font1">Diário</span> <span class="font2">Livre</span>'.html_safe
  end

  def linkQuestionario
    'http://devcolab.each.usp.br/limesurvey/index.php/191978'.html_safe
  end

  def gerarCreditosMK
    lista = [
      'Andrés M. R. Martano',
      'Rafael Santana',
      'Larissa Y. Oyadomari',
      'Gisele S. Craveiro',
      'Jorge Machado',
      'Nahema Nascimento Barra de Oliveira',
      'Emerson Marques Pedro',
      'Fabiano Angélico',
      'Gabriel Ponzetto',
      'Givanildo Andrade Lopes',
      'Fernanda Campagnucci',
      'Clarissa Carmona',
      'Alice Fernanda Dias Gonçalves',
      'Renato Mataruco Lopes',
      'José de Jesús Pérez-Al',
      'Selma Berezutchi',
      'Paulo Roberto Dutra',
      'Danilo Marasca Bertazzi',
      'Domingas Soares de Oliveira',
    ].sort! .collect { |x| "<li>%s</li>" % x } .join "\n"
  end

end
